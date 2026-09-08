"""
agents/base_agent.py

Abstract contract every member of the Swarm (Radar Scout, Visionary, Order
Book Sniper, Whisperer, and any future agent) must implement.

The pattern is deliberately the same three verbs described in the original
architecture: **subscribe -> analyze -> publish**.

    - `input_channels` (subscribe): which Redis channels this agent cares
      about. `BaseAgent` handles fanning in from all of them concurrently.
    - `analyze` (analyze): the one method subclasses actually implement —
      "given this one incoming event, do your specialized thing."
    - `publish` (publish): a thin helper subclasses call from inside
      `analyze` to emit zero, one, or many results, to whichever channel(s)
      makes sense for that result (an agent might publish alerts to one
      channel and opinions to another).

This mirrors `core/data_feed/base_feed.py`'s shape on purpose: both are
"long-running background worker with a start/stop lifecycle and automatic
resilience" — an agent's resilience concern is just "don't let one bad
event or one dropped Redis connection kill the whole agent," which is
exactly what `RedisEventBus.subscribe()` and the try/except in
`_consume_channel` below provide.
"""

from __future__ import annotations

import asyncio
import logging
from abc import ABC, abstractmethod
from enum import Enum

from pydantic import BaseModel

from core.event_bus.redis_bus import RedisEventBus

logger = logging.getLogger(__name__)


class AgentStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    ERROR = "error"
    STOPPED = "stopped"


class BaseAgent(ABC):
    """
    Abstract base class for all Swarm agents.

    Parameters
    ----------
    event_bus:
        The shared `RedisEventBus` instance. Injected rather than
        constructed internally, so agents are trivially testable with a
        fake bus and so every agent in the process shares one physical
        Redis connection.
    """

    def __init__(self, event_bus: RedisEventBus) -> None:
        self.event_bus = event_bus
        self._status: AgentStatus = AgentStatus.IDLE
        self._stop_event: asyncio.Event = asyncio.Event()
        self._tasks: list[asyncio.Task] = []

    # ------------------------------------------------------------------
    # Contract subclasses must implement
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def name(self) -> str:
        """Short, unique identifier for this agent, e.g. 'radar_scout'.
        Used in logging, task naming, and as the `source` field on any
        events this agent publishes."""
        raise NotImplementedError

    @property
    @abstractmethod
    def input_channels(self) -> list[str]:
        """Redis channels this agent subscribes to. Evaluated once at
        `start()` time — if an agent's watchlist changes at runtime, it
        should be restarted (`stop()` then `start()`) to resubscribe."""
        raise NotImplementedError

    @abstractmethod
    async def analyze(self, event: BaseModel) -> None:
        """
        Process one incoming event from any of `input_channels`.

        Implementations should call `await self.publish(channel, result)`
        zero or more times as needed — this method's return value is
        ignored. Raising here is reserved for genuinely unexpected
        failures: `BaseAgent` will log and swallow the exception so one bad
        event can't take down the agent's subscription loop, but repeated
        exceptions likely mean a real bug worth fixing, not a supported
        control-flow path.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Shared helper for subclasses
    # ------------------------------------------------------------------

    async def publish(self, channel: str, event: BaseModel) -> None:
        """Publish one result event to `channel` via the shared event bus."""
        await self.event_bus.publish(channel, event)

    # ------------------------------------------------------------------
    # Lifecycle — subclasses should not need to override these.
    # ------------------------------------------------------------------

    @property
    def status(self) -> AgentStatus:
        return self._status

    async def start(self) -> None:
        """Begin consuming `input_channels` in the background. Safe to call
        once; call `stop()` before calling `start()` again."""
        if self._tasks:
            logger.warning("%s.start() called while already running.", self.name)
            return

        self._stop_event.clear()
        self._tasks = [
            asyncio.create_task(self._consume_channel(channel), name=f"{self.name}:{channel}")
            for channel in self.input_channels
        ]
        self._status = AgentStatus.RUNNING
        logger.info(
            "Agent '%s' started, listening on %d channel(s).",
            self.name,
            len(self._tasks),
        )

    async def stop(self) -> None:
        """Signal all subscription loops to stop and wait for them to exit."""
        self._stop_event.set()
        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks = []
        self._status = AgentStatus.STOPPED
        logger.info("Agent '%s' stopped.", self.name)

    # ------------------------------------------------------------------
    # Internal: one fan-in loop per subscribed channel
    # ------------------------------------------------------------------

    async def _consume_channel(self, channel: str) -> None:
        try:
            async for event in self.event_bus.subscribe(channel):
                if self._stop_event.is_set():
                    break
                try:
                    await self.analyze(event)
                except asyncio.CancelledError:
                    raise
                except Exception:  # noqa: BLE001 - one bad event must not
                    # kill this agent's subscription loop.
                    self._status = AgentStatus.ERROR
                    logger.exception(
                        "%s: error analyzing event from '%s'.", self.name, channel
                    )
                    self._status = AgentStatus.RUNNING
        except asyncio.CancelledError:
            logger.debug("%s: subscription loop on '%s' cancelled.", self.name, channel)
            raise
