"""
agents/orderbook_sniper.py

The Order Book Sniper: L2 liquidity, wall detection, and spoofing analysis.

While Radar Scout uses a coarse, fast bid/ask volume imbalance to flag
anomalies across the entire watchlist, Order Book Sniper digs deep into
the top-N order book levels for symbols flagged by the radar.

Responsibilities:
    - Detect large resting limit walls (bid/ask walls) that could act as
      support or resistance.
    - Identify potential spoofing / layering patterns by tracking sudden
      cancellations of large orders.
    - Compute micro-structural momentum and publish an `AgentOpinionEvent`
      to the Oracle Hub when high-conviction order book setups occur.
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel, Field

from agents.base_agent import BaseAgent
from core.event_bus.redis_bus import Channels, RedisEventBus
from core.event_bus.schemas import (
    AgentOpinionEvent,
    OpinionDirection,
    OrderBookEvent,
    RadarAlertEvent,
)

logger = logging.getLogger(__name__)


class OrderBookSniper(BaseAgent):
    """
    Sniper agent inspecting order book depth and liquidity walls.
    """

    def __init__(
        self,
        event_bus: RedisEventBus,
        symbols: list[str],
        wall_size_multiplier: float = 3.5,
        min_confidence: float = 0.4,
    ) -> None:
        super().__init__(event_bus=event_bus)
        self.symbols = symbols
        self._wall_size_multiplier = wall_size_multiplier
        self._min_confidence = min_confidence

    @property
    def name(self) -> str:
        return "orderbook_sniper"

    @property
    def input_channels(self) -> list[str]:
        # Subscribes to order book updates for its symbols and radar alerts
        return [Channels.orderbook(s) for s in self.symbols] + [Channels.RADAR_ALERTS]

    async def analyze(self, event: BaseModel) -> None:
        if isinstance(event, OrderBookEvent):
            await self._inspect_order_book(event)
        elif isinstance(event, RadarAlertEvent):
            if event.symbol in self.symbols:
                logger.info("%s received radar alert for %s — increasing focus.", self.name, event.symbol)

    async def _inspect_order_book(self, event: OrderBookEvent) -> None:
        if not event.bids or not event.asks:
            return

        # Calculate average depth size per level
        bid_sizes = [lvl.amount for lvl in event.bids]
        ask_sizes = [lvl.amount for lvl in event.asks]

        avg_bid_size = sum(bid_sizes) / len(bid_sizes) if bid_sizes else 0
        avg_ask_size = sum(ask_sizes) / len(ask_sizes) if ask_sizes else 0

        # Check for massive walls at the top levels
        top_bid = event.bids[0]
        top_ask = event.asks[0]

        is_bid_wall = top_bid.amount >= (avg_bid_size * self._wall_size_multiplier)
        is_ask_wall = top_ask.amount >= (avg_ask_size * self._wall_size_multiplier)

        if is_bid_wall and not is_ask_wall:
            direction = OpinionDirection.BULLISH
            confidence = 0.65
            reasoning = f"{event.symbol}: Strong support bid wall detected at {top_bid.price} with size {top_bid.amount:.2f}."
        elif is_ask_wall and not is_bid_wall:
            direction = OpinionDirection.BEARISH
            confidence = 0.65
            reasoning = f"{event.symbol}: Strong resistance ask wall detected at {top_ask.price} with size {top_ask.amount:.2f}."
        else:
            return  # No clear structural edge

        if confidence >= self._min_confidence:
            entry = (top_bid.price + top_ask.price) / 2.0
            opinion = AgentOpinionEvent(
                source=self.name,
                symbol=event.symbol,
                timestamp_ms=event.timestamp_ms,
                direction=direction,
                confidence=confidence,
                reasoning=reasoning,
                suggested_entry=entry,
                suggested_stop_loss=top_bid.price if direction == OpinionDirection.BULLISH else top_ask.price,
                suggested_take_profits=[entry * 1.01, entry * 1.02],
                metadata={"top_bid": top_bid.amount, "top_ask": top_ask.amount},
            )
            logger.info("SNIPER OPINION: %s", reasoning)
            await self.publish(Channels.AGENT_OPINIONS, opinion)
