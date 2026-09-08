from __future__ import annotations
from pydantic import BaseModel
from enum import Enum

class OpinionDirection(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"

class RadarAlertType(str, Enum):
    VOLUME_SPIKE = "volume_spike"
    RSI_EXTREME = "rsi_extreme"
    PRICE_BREAKOUT = "price_breakout"

class TickEvent(BaseModel):
    symbol: str
    price: float
    timestamp_ms: int

class OHLCVEvent(BaseModel):
    symbol: str
    timeframe: str
    timestamp_ms: int
    open: float
    high: float
    low: float
    close: float
    volume: float

class OrderBookLevel(BaseModel):
    price: float
    amount: float

class OrderBookEvent(BaseModel):
    symbol: str
    timestamp_ms: int
    bids: list[OrderBookLevel]
    asks: list[OrderBookLevel]

class RadarAlertEvent(BaseModel):
    symbol: str
    timestamp_ms: int
    alert_type: RadarAlertType = RadarAlertType.VOLUME_SPIKE
    reason: str

class AgentOpinionEvent(BaseModel):
    source: str
    symbol: str
    timestamp_ms: int
    direction: OpinionDirection
    confidence: float
    reasoning: str
    suggested_entry: float | None = None
    suggested_stop_loss: float | None = None
    suggested_take_profits: list[float] = []
    metadata: dict = {}

EVENT_TYPE_REGISTRY = {
    "tick": TickEvent,
    "ohlcv": OHLCVEvent,
    "orderbook": OrderBookEvent,
    "radar_alert": RadarAlertEvent,
    "agent_opinion": AgentOpinionEvent,
}
