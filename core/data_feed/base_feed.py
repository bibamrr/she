"""
core/data_feed/base_feed.py

Abstract contract that every market data feed (crypto, US equities, or
future asset classes) must implement.

Why an abstract base class here matters architecturally: nothing downstream
(the event bus, the agents, the Oracle Hub) should ever import
`CCXTFeed` or `IBKRFeed` directly. They should depend on `BaseFeed`. This is
the Dependency Inversion half of SOLID — swapping Binance for Coinbase, or
adding a new stock broker, becomes "write a new subclass", not "touch every
consumer of market data".

A `BaseFeed` implementation is responsible ONLY for:
    1. Connecting to its upstream source (WebSocket, FIX, etc).
    2. Normalizing whatever wire format it receives into our internal
       Pydantic event schemas (`core.event_bus.schemas`).
    3. Publishing those normalized events onto the shared event bus.
    4. Reconnecting itself when the connection drops.

It is explicitly NOT responsible for indicator calculation, signal
generation, or persistence — those live in `indicators/`, `agents/`, and
`persistence/` respectively.
"""

from __future__ import annotations

import asyncio
import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterable

from core.event_bus.schemas import OrderBookEvent, OHLCVEvent, TickEvent

logger = logging.getLogger(__name__)


class FeedStatus(str, Enum):
    """Lifecycle states for a feed connection, exposed so monitoring /
    the frontend can show connection health per-exchange."""

    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"
    ERROR = "error"
    STOPPED = "stopped"


class BaseFeed(ABC):
    """
    Abstract base class for all real-time market data feeds.

    Subclasses must implement the four abstract methods below. Everything
    else (status tracking, the public `start`/`stop` lifecycle, and the
    reconnect-with-backoff loop) is provided here so concrete feeds don't
    each reinvent reconnection logic.

    Parameters
    ----------
    symbols:
        Unified-format symbols this feed instance should subscribe to,
        e.g. ["BTC/USDT", "ETH/USDT"].
    timeframes:
        Candle timeframes to subscribe to for OHLCV streams, e.g. ["1m", "5m"].
    max_backoff_seconds:
        Ceiling for the exponential reconnect backoff, so a prolonged outage
        doesn't leave us hammering the exchange every few milliseconds nor
        waiting forever between attempts.
    """

    def __init__(
        self,
        symbols: Iterable[str],
        timeframes: Iterable[str] | None = None,
        max_backoff_seconds: float = 60.0,
    ) -> None:
        self.symbols: list[str] = list(symbols)
        self.timeframes: list[str] = list(timeframes or [])
        self._max_backoff_seconds = max_backoff_seconds
        self._status: FeedStatus = FeedStatus.DISCONNECTED
        self._stop_event: asyncio.Event = asyncio.Event()
        self._run_task: asyncio.Task | None = None

    # ------------------------------------------------------------------
    # Public lifecycle API — concrete subclasses should NOT override these.
    # ------------------------------------------------------------------

    async def start(self) -> None:
        """Begin streaming in the background. Safe to call once; call
        `stop()` before calling `start()` again."""
        if self._run_task is not None and not self._run_task.done():
            logger.warning("%s.start() called while already running.", self.name)
            return

        self._stop_event.clear()
        self._run_task = asyncio.create_task(
            self._run_with_reconnect(), name=f"feed:{self.name}"
        )
        logger.info(
            "Started feed '%s' for symbols=%s timeframes=%s",
            self.name,
            self.symbols,
            self.timeframes,
        )

    async def stop(self) -> None:
        """Signal the feed to shut down gracefully and wait for it to exit."""
        self._stop_event.set()
        if self._run_task is not None:
            await asyncio.wait_for(self._run_task, timeout=30)
        self._status = FeedStatus.STOPPED
        logger.info("Stopped feed '%s'.", self.name)

    @property
    def status(self) -> FeedStatus:
        return self._status

    @property
    @abstractmethod
    def name(self) -> str:
        """Short, unique identifier for this feed, e.g. 'binance-ccxt'."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Reconnect-with-backoff wrapper around the subclass's `_connect_and_stream`.
    # ------------------------------------------------------------------

    async def _run_with_reconnect(self) -> None:
        backoff = 1.0
        while not self._stop_event.is_set():
            try:
                self._status = FeedStatus.CONNECTING
                await self._connect_and_stream()
                # A clean return from _connect_and_stream (rather than an
                # exception) means the subclass decided to stop on its own.
                break
            except asyncio.CancelledError:
                raise
            except Exception:  # noqa: BLE001 - deliberately broad: any feed
                # error must trigger reconnect, not crash the whole process.
                self._status = FeedStatus.ERROR
                logger.exception(
                    "Feed '%s' errored; reconnecting in %.1fs.",
                    self.name,
                    backoff,
                )
                self._status = FeedStatus.RECONNECTING
                try:
                    await asyncio.wait_for(self._stop_event.wait(), timeout=backoff)
                except asyncio.TimeoutError:
                    pass  # normal: backoff elapsed, loop again
                backoff = min(backoff * 2, self._max_backoff_seconds)
                continue
            else:
                backoff = 1.0  # reset after a clean cycle if we ever loop

    # ------------------------------------------------------------------
    # Abstract methods — every concrete feed must implement these.
    # ------------------------------------------------------------------

    @abstractmethod
    async def _connect_and_stream(self) -> None:
        """
        Open the upstream connection and stream data until either:
            - `self._stop_event` is set (check it periodically), or
            - an exception is raised (the reconnect wrapper will catch it).

        Implementations should call `self._emit_tick`, `self._emit_ohlcv`,
        and/or `self._emit_orderbook` as data arrives.
        """
        raise NotImplementedError

    @abstractmethod
    async def _emit_tick(self, event: TickEvent) -> None:
        """Publish a normalized tick event to the event bus."""
        raise NotImplementedError

    @abstractmethod
    async def _emit_ohlcv(self, event: OHLCVEvent) -> None:
        """Publish a normalized OHLCV bar event to the event bus."""
        raise NotImplementedError

    @abstractmethod
    async def _emit_orderbook(self, event: OrderBookEvent) -> None:
        """Publish a normalized order book snapshot/delta to the event bus."""
        raise NotImplementedError
