"""
core/event_bus/redis_bus.py

Event Bus abstraction with in-memory fallback and correct argument signatures.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Callable

from config.settings import Settings

logger = logging.getLogger(__name__)


class CallableChannelStr(str):
    def __call__(self, *args: Any, **kwargs: Any) -> str:
        if args:
            return self.format(*args, **kwargs)
        return str(self)


class Channels:
    TICK_DATA = "ticks"
    OHLCV_DATA = "ohlcv"
    ORDER_BOOK = "orderbook"
    RADAR_ALERTS = "radar_alerts"
    AGENT_OPINIONS = "agent_opinions"
    TRADE_SIGNALS = "trade_signals"

    ticks = CallableChannelStr("ticks")
    ohlcv = CallableChannelStr("{}_{}")
    orderbook = CallableChannelStr("orderbook")
    radar_alerts = CallableChannelStr("radar_alerts")
    agent_opinions = CallableChannelStr("agent_opinions")
    trade_signals = CallableChannelStr("trade_signals")

    @classmethod
    def __getattr__(cls, name: str) -> CallableChannelStr:
        return CallableChannelStr(name)


class RedisEventBus:
    """
    In-memory fallback event bus simulating pub/sub behavior for standalone execution.
    """

    def __init__(self, host: str, port: int, db: int = 0) -> None:
        self.host = host
        self.port = port
        self.db = db
        self.subscribers: dict[str, list[Callable]] = {}
        self._connected = False

    @classmethod
    def from_settings(cls, settings: Settings) -> RedisEventBus:
        return cls(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
        )

    async def connect(self) -> None:
        self._connected = True
        logger.info("Connected to In-Memory Event Bus (Standalone Mode).")

    async def close(self) -> None:
        self._connected = False
        logger.info("Closed In-Memory Event Bus.")

    async def publish(self, channel: str, message: Any) -> None:
        if not self._connected:
            return
        
        if hasattr(message, "model_dump"):
            payload = message.model_dump()
        elif hasattr(message, "dict"):
            payload = message.dict()
        else:
            payload = message

        callbacks = self.subscribers.get(channel, [])
        for cb in callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    asyncio.create_task(cb(payload))
                else:
                    cb(payload)
            except Exception as e:
                logger.error("Error in subscriber callback for channel %s: %s", channel, e)

    async def publish_market_data(self, channel: str, message: Any) -> None:
        """Accepts both channel and message correctly."""
        await self.publish(channel, message)

    async def subscribe(self, channel: str, callback: Callable[[Any], Any]) -> None:
        if channel not in self.subscribers:
            self.subscribers[channel] = []
        self.subscribers[channel].append(callback)
        logger.info("Subscribed to channel: %s", channel)
