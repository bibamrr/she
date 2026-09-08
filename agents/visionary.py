"""
agents/visionary.py

The Visionary Agent: multi-timeframe technical analysis.

Unlike Radar Scout (cheap, always-on, single-timeframe screening),
Visionary maintains a rolling candle history across SEVERAL timeframes per
symbol and only runs its (comparatively expensive) full analysis when
triggered — either by a `RadarAlertEvent` ("something's happening on this
symbol, go look closer") or, less commonly, on a direct request from the
Oracle Hub in a later phase.

What "full analysis" means here, per timeframe:
    - Trend bias from EMA(fast) vs EMA(slow) crossover state.
    - Momentum bias from MACD histogram sign/direction.
    - RSI level (context, not a standalone trigger at this stage).
    - A lightweight linear-regression trend slope (a proxy for "is this
      timeframe trending or ranging" — see the honesty note below).
    - A small classical-pattern check (bullish/bearish engulfing on the
      last two closed candles).

Those per-timeframe verdicts are combined into one overall direction via a
weighted vote — larger timeframes get more weight, since a 1h uptrend
matters more than 1m noise — and packaged into an `AgentOpinionEvent` with
a concrete suggested entry/SL/tiered-TP, derived from ATR on the
"execution timeframe" (the timeframe actually used for entry timing).

Honesty note on scope: the trend-slope and engulfing checks here are
deliberately simple, self-contained proxies for "trendlines and classical
patterns" — not a full swing-high/low trendline-drawing engine or a
20-pattern candlestick library. They're accurate for what they claim to
detect, and this module is structured so a real pattern-recognition module
can be dropped in later as `_detect_pattern`'s replacement without
touching anything else here.
"""

from __future__ import annotations

import logging
import math
from collections import deque
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from pydantic import BaseModel

from agents.base_agent import BaseAgent
from core.event_bus.redis_bus import Channels, RedisEventBus
from core.event_bus.schemas import (
    AgentOpinionEvent,
    OHLCVEvent,
    OpinionDirection,
    RadarAlertEvent,
)
from indicators.momentum import ema, macd, rsi
from indicators.volatility import atr

logger = logging.getLogger(__name__)


def _timeframe_to_minutes(timeframe: str) -> int:
    """Parse ccxt-style timeframe strings ('1m', '15m', '4h', '1d') into
    minutes, used purely to derive a relative weight — larger timeframes
    should influence the combined verdict more than smaller ones."""
    unit_minutes = {"m": 1, "h": 60, "d": 1440, "w": 10080}
    unit = timeframe[-1]
    if unit not in unit_minutes:
        raise ValueError(f"Unrecognized timeframe unit in '{timeframe}'.")
    return int(timeframe[:-1]) * unit_minutes[unit]


def _timeframe_weight(timeframe: str) -> float:
    """Log-scaled weight so a 1h timeframe outweighs a 1m one without
    completely drowning it out (a raw-minutes weight would make 1h worth
    60x a 1m reading, which overstates the case)."""
    return math.log2(_timeframe_to_minutes(timeframe) + 1) + 1.0


@dataclass
class _CandleBuffer:
    """Rolling window of CLOSED candles for one (symbol, timeframe) pair."""

    maxlen: int
    candles: deque[OHLCVEvent] = field(init=False)

    def __post_init__(self) -> None:
        self.candles = deque(maxlen=self.maxlen)

    def push_closed(self, candle: OHLCVEvent) -> None:
        self.candles.append(candle)

    def to_dataframe(self) -> pd.DataFrame:
        """Materialize the buffer as a DataFrame, oldest row first, ready
        for the vectorized indicator functions in `indicators/`."""
        return pd.DataFrame(
            {
                "timestamp_ms": [c.timestamp_ms for c in self.candles],
                "open": [c.open for c in self.candles],
                "high": [c.high for c in self.candles],
                "low": [c.low for c in self.candles],
                "close": [c.close for c in self.candles],
                "volume": [c.volume for c in self.candles],
            }
        )


@dataclass
class _TimeframeVerdict:
    timeframe: str
    direction: OpinionDirection
    rsi_value: float
    macd_histogram: float
    pattern: str | None
    weight: float


def _detect_engulfing(df: pd.DataFrame) -> str | None:
    """Lightweight bullish/bearish engulfing check on the last two closed
    candles. See module docstring's honesty note on scope."""
    if len(df) < 2:
        return None
    prev, curr = df.iloc[-2], df.iloc[-1]

    prev_bearish = prev["close"] < prev["open"]
    curr_bullish = curr["close"] > curr["open"]
    if prev_bearish and curr_bullish and curr["close"] >= prev["open"] and curr["open"] <= prev["close"]:
        return "bullish_engulfing"

    prev_bullish = prev["close"] > prev["open"]
    curr_bearish = curr["close"] < curr["open"]
    if prev_bullish and curr_bearish and curr["open"] >= prev["close"] and curr["close"] <= prev["open"]:
        return "bearish_engulfing"

    return None


def _trend_slope_direction(closes: pd.Series, flat_threshold: float = 0.0005) -> OpinionDirection:
    """
    Linear-regression slope of closes, normalized by mean price so it's
    comparable across symbols of very different price scales. This is a
    coarse "is this timeframe trending up/down/sideways" proxy, not a
    substitute for real trendline (swing-high/low) analysis.
    """
    if len(closes) < 3:
        return OpinionDirection.NEUTRAL
    x = np.arange(len(closes))
    slope, _intercept = np.polyfit(x, closes.to_numpy(), deg=1)
    normalized_slope = slope / closes.mean()
    if normalized_slope > flat_threshold:
        return OpinionDirection.BULLISH
    if normalized_slope < -flat_threshold:
        return OpinionDirection.BEARISH
    return OpinionDirection.NEUTRAL


class VisionaryAgent(BaseAgent):
    """
    Parameters
    ----------
    event_bus:
        Shared `RedisEventBus`.
    symbols:
        Symbols this instance covers.
    timeframes:
        Timeframes to maintain rolling buffers for and analyze, e.g.
        `["1m", "5m", "15m", "1h"]`. Order does not matter.
    execution_timeframe:
        Which of `timeframes` supplies the candle used for the concrete
        suggested entry price and the ATR used for stop sizing. Should
        generally be your shortest/most granular timeframe.
    buffer_size:
        How many closed candles to retain per (symbol, timeframe).
    ema_fast_period / ema_slow_period:
        EMA crossover periods for the per-timeframe trend bias.
    rsi_period, atr_period, atr_multiplier:
        Passed straight through to `indicators.momentum.rsi` /
        `indicators.volatility.atr_stop_distance`.
    take_profit_r_multiples:
        Tiered TP targets in R-multiples of the ATR-based stop distance.
        Mirrors `config.settings.RiskThresholds.take_profit_r_multiples`
        by default but is passed explicitly here rather than importing
        `Settings` directly, keeping this agent unit-testable in isolation.
    min_confidence_to_publish:
        Below this, Visionary still logs its reasoning but does not
        publish an opinion — a wishy-washy NEUTRAL read on every alert
        would just add noise for the Oracle Hub.
    """

    def __init__(
        self,
        event_bus: RedisEventBus,
        symbols: list[str],
        timeframes: list[str],
        execution_timeframe: str,
        buffer_size: int = 200,
        ema_fast_period: int = 12,
        ema_slow_period: int = 26,
        rsi_period: int = 14,
        atr_period: int = 14,
        atr_multiplier: float = 1.5,
        take_profit_r_multiples: list[float] | None = None,
        min_confidence_to_publish: float = 0.2,
    ) -> None:
        super().__init__(event_bus=event_bus)
        if execution_timeframe not in timeframes:
            raise ValueError("execution_timeframe must be one of `timeframes`.")

        self.symbols = symbols
        self.timeframes = timeframes
        self.execution_timeframe = execution_timeframe
        self._ema_fast_period = ema_fast_period
        self._ema_slow_period = ema_slow_period
        self._rsi_period = rsi_period
        self._atr_period = atr_period
        self._atr_multiplier = atr_multiplier
        self._take_profit_r_multiples = take_profit_r_multiples or [1.0, 2.0, 3.0]
        self._min_confidence_to_publish = min_confidence_to_publish

        # Warm-up requirement: enough candles for the slowest indicator
        # (EMA-slow/MACD/RSI/ATR) to produce a non-NaN reading.
        self._min_candles_required = max(ema_slow_period, rsi_period, atr_period) + 5

        self._buffers: dict[tuple[str, str], _CandleBuffer] = {
            (symbol, tf): _CandleBuffer(maxlen=buffer_size)
            for symbol in symbols
            for tf in timeframes
        }
        # Latest not-yet-confirmed-closed candle per (symbol, timeframe).
        self._pending: dict[tuple[str, str], OHLCVEvent] = {}

    @property
    def name(self) -> str:
        return "visionary"

    @property
    def input_channels(self) -> list[str]:
        ohlcv_channels = [
            Channels.ohlcv(symbol, tf) for symbol in self.symbols for tf in self.timeframes
        ]
        return ohlcv_channels + [Channels.RADAR_ALERTS]

    async def analyze(self, event: BaseModel) -> None:
        if isinstance(event, OHLCVEvent):
            await self._update_buffer(event)
        elif isinstance(event, RadarAlertEvent):
            if event.symbol in self.symbols:
                await self._run_full_analysis(event.symbol)

    # ------------------------------------------------------------------
    # Passive buffer maintenance (cheap — runs on every candle update)
    # ------------------------------------------------------------------

    async def _update_buffer(self, event: OHLCVEvent) -> None:
        key = (event.symbol, event.timeframe)
        if key not in self._buffers:
            return  # not a (symbol, timeframe) combination we track

        pending = self._pending.get(key)
        if pending is not None and pending.timestamp_ms != event.timestamp_ms:
            # A new bar started -> the previous one is now final.
            self._buffers[key].push_closed(pending)
        self._pending[key] = event

    # ------------------------------------------------------------------
    # Active analysis (expensive-ish — runs only when Radar Scout triggers)
    # ------------------------------------------------------------------

    async def _run_full_analysis(self, symbol: str) -> None:
        verdicts: list[_TimeframeVerdict] = []

        for tf in self.timeframes:
            df = self._buffers[(symbol, tf)].to_dataframe()
            if len(df) < self._min_candles_required:
                logger.debug(
                    "%s: skipping %s/%s — only %d/%d candles buffered.",
                    self.name,
                    symbol,
                    tf,
                    len(df),
                    self._min_candles_required,
                )
                continue
            verdicts.append(self._analyze_timeframe(tf, df))

        if not verdicts:
            logger.info(
                "%s: no timeframe had enough history yet for %s; skipping this trigger.",
                self.name,
                symbol,
            )
            return

        direction, confidence = self._combine_verdicts(verdicts)
        reasoning = self._build_reasoning(symbol, verdicts, direction, confidence)

        if confidence < self._min_confidence_to_publish:
            logger.info(
                "%s: confidence %.2f for %s below publish threshold; logging only.\n%s",
                self.name,
                confidence,
                symbol,
                reasoning,
            )
            return

        entry, stop_loss, take_profits = self._build_trade_levels(symbol, direction)

        opinion = AgentOpinionEvent(
            source=self.name,
            symbol=symbol,
            timestamp_ms=int(
                self._buffers[(symbol, self.execution_timeframe)].candles[-1].timestamp_ms
            ),
            direction=direction,
            confidence=round(confidence, 3),
            reasoning=reasoning,
            suggested_entry=entry,
            suggested_stop_loss=stop_loss,
            suggested_take_profits=take_profits,
            metadata={f"{v.timeframe}_rsi": v.rsi_value for v in verdicts},
        )
        logger.info("VISIONARY OPINION: %s", reasoning)
        await self.publish(Channels.AGENT_OPINIONS, opinion)

    def _analyze_timeframe(self, timeframe: str, df: pd.DataFrame) -> _TimeframeVerdict:
        closes = df["close"]
        ema_fast_series = ema(closes, self._ema_fast_period)
        ema_slow_series = ema(closes, self._ema_slow_period)
        macd_df = macd(closes)
        rsi_series = rsi(closes, self._rsi_period)

        ema_fast_now = ema_fast_series.iloc[-1]
        ema_slow_now = ema_slow_series.iloc[-1]
        histogram_now = macd_df["histogram"].iloc[-1]
        rsi_now = rsi_series.iloc[-1]

        ema_bias = (
            OpinionDirection.BULLISH if ema_fast_now > ema_slow_now else OpinionDirection.BEARISH
        )
        macd_bias = OpinionDirection.BULLISH if histogram_now > 0 else OpinionDirection.BEARISH
        slope_bias = _trend_slope_direction(closes.tail(30))

        # Simple 2-of-3 vote among the three sub-signals for this timeframe.
        biases = [ema_bias, macd_bias, slope_bias]
        bullish_votes = biases.count(OpinionDirection.BULLISH)
        bearish_votes = biases.count(OpinionDirection.BEARISH)
        if bullish_votes > bearish_votes:
            direction = OpinionDirection.BULLISH
        elif bearish_votes > bullish_votes:
            direction = OpinionDirection.BEARISH
        else:
            direction = OpinionDirection.NEUTRAL

        pattern = _detect_engulfing(df)

        return _TimeframeVerdict(
            timeframe=timeframe,
            direction=direction,
            rsi_value=float(rsi_now),
            macd_histogram=float(histogram_now),
            pattern=pattern,
            weight=_timeframe_weight(timeframe),
        )

    @staticmethod
    def _combine_verdicts(verdicts: list[_TimeframeVerdict]) -> tuple[OpinionDirection, float]:
        """Weighted vote across timeframes. Returns (direction, confidence),
        where confidence is the magnitude of agreement in [0, 1]."""
        total_weight = sum(v.weight for v in verdicts)
        score = 0.0
        for v in verdicts:
            if v.direction == OpinionDirection.BULLISH:
                score += v.weight
            elif v.direction == OpinionDirection.BEARISH:
                score -= v.weight
        normalized_score = score / total_weight if total_weight else 0.0

        if normalized_score > 0.15:
            direction = OpinionDirection.BULLISH
        elif normalized_score < -0.15:
            direction = OpinionDirection.BEARISH
        else:
            direction = OpinionDirection.NEUTRAL

        # A pattern match on ANY timeframe nudges confidence up slightly —
        # it's corroborating evidence, not a standalone trigger.
        pattern_bonus = 0.05 if any(v.pattern is not None for v in verdicts) else 0.0
        confidence = min(1.0, abs(normalized_score) + pattern_bonus)
        return direction, confidence

    def _build_trade_levels(
        self, symbol: str, direction: OpinionDirection
    ) -> tuple[float | None, float | None, list[float]]:
        if direction == OpinionDirection.NEUTRAL:
            return None, None, []

        exec_df = self._buffers[(symbol, self.execution_timeframe)].to_dataframe()
        entry = float(exec_df["close"].iloc[-1])
        atr_now = atr(exec_df, period=self._atr_period).iloc[-1]
        if pd.isna(atr_now) or atr_now <= 0:
            logger.warning(
                "%s: ATR unavailable/non-positive for %s on %s; omitting SL/TP levels.",
                self.name,
                symbol,
                self.execution_timeframe,
            )
            return entry, None, []

        stop_distance = float(atr_now) * self._atr_multiplier
        if direction == OpinionDirection.BULLISH:
            stop_loss = entry - stop_distance
            take_profits = [entry + m * stop_distance for m in self._take_profit_r_multiples]
        else:
            stop_loss = entry + stop_distance
            take_profits = [entry - m * stop_distance for m in self._take_profit_r_multiples]

        return entry, stop_loss, take_profits

    @staticmethod
    def _build_reasoning(
        symbol: str,
        verdicts: list[_TimeframeVerdict],
        direction: OpinionDirection,
        confidence: float,
    ) -> str:
        per_tf = "; ".join(
            f"{v.timeframe}={v.direction.value}"
            f"(RSI {v.rsi_value:.0f}, MACD-hist {v.macd_histogram:+.4f}"
            + (f", {v.pattern}" if v.pattern else "")
            + ")"
            for v in verdicts
        )
        return (
            f"{symbol}: combined multi-timeframe verdict = {direction.value.upper()} "
            f"(confidence {confidence:.2f}). Per-timeframe: {per_tf}."
        )
