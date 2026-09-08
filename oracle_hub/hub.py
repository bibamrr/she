"""
oracle_hub/hub.py

The Oracle Hub: Central decision-making engine using LangGraph.

Responsibilities:
    - Listen for agent opinions (`Channels.AGENT_OPINIONS`).
    - Aggregate opinions per symbol within a rolling time window.
    - Resolve conflicts (e.g., Visionary says BULLISH, Sniper says BEARISH).
    - Consult the RiskEngine for position sizing and final approval.
    - Emit final execution signals (`Channels.TRADE_SIGNALS`).
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel, Field

from core.event_bus.redis_bus import Channels, RedisEventBus
from core.event_bus.schemas import AgentOpinionEvent, OpinionDirection
from core.risk.risk_engine import RiskEngine

logger = logging.getLogger(__name__)


class TradeSignalEvent(BaseModel):
    """Final output emitted by the Oracle Hub when a trade is approved."""

    symbol: str
    direction: OpinionDirection
    entry_price: float
    stop_loss: float
    take_profits: list[float]
    position_size: float
    confidence: float
    reasoning: str


class OracleHub:
    """
    Central coordinator aggregating agent opinions and enforcing risk rules.
    """

    def __init__(self, event_bus: RedisEventBus, risk_engine: RiskEngine) -> None:
        self.event_bus = event_bus
        self.risk_engine = risk_engine

    async def evaluate_opinions(
        self,
        opinions: list[AgentOpinionEvent],
        account_equity: float,
        open_positions_count: int,
    ) -> TradeSignalEvent | None:
        """
        Consensus algorithm: aggregates multiple agent opinions for a symbol.
        """
        if not opinions:
            return None

        symbol = opinions[0].symbol
        
        # Simple weighted consensus based on agent confidence
        bullish_score = sum(op.confidence for op in opinions if op.direction == OpinionDirection.BULLISH)
        bearish_score = sum(op.confidence for op in opinions if op.direction == OpinionDirection.BEARISH)

        if bullish_score > bearish_score and bullish_score >= 0.5:
            direction = OpinionDirection.BULLISH
        elif bearish_score > bullish_score and bearish_score >= 0.5:
            direction = OpinionDirection.BEARISH
        else:
            return None  # No consensus or neutral

        # Pick the best reference price levels from the highest confidence opinion
        best_opinion = max(opinions, key=lambda o: o.confidence)
        if not best_opinion.suggested_entry or not best_opinion.suggested_stop_loss:
            return None

        # Validate through Risk Engine
        is_approved, position_size, reason = self.risk_engine.evaluate_trade(
            account_equity=account_equity,
            current_open_positions=open_positions_count,
            entry_price=best_opinion.suggested_entry,
            stop_loss_price=best_opinion.suggested_stop_loss,
        )

        if not is_approved:
            logger.warning("Trade rejected by RiskEngine for %s: %s", symbol, reason)
            return None

        signal = TradeSignalEvent(
            symbol=symbol,
            direction=direction,
            entry_price=best_opinion.suggested_entry,
            stop_loss=best_opinion.suggested_stop_loss,
            take_profits=best_opinion.suggested_take_profits,
            position_size=position_size,
            confidence=best_opinion.confidence,
            reasoning=f"Consensus reached. {best_opinion.reasoning}",
        )
        
        await self.event_bus.publish(Channels.TRADE_SIGNALS, signal)
        logger.info("TRADE SIGNAL ISSUED: %s %s size=%.4f", direction.value, symbol, position_size)
        return signal
