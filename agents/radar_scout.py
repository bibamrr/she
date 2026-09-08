"""
agents/radar_scout.py

The Hunter: a lightweight, always-on screener across the entire watchlist.

RadarScout deliberately does NOT do deep analysis — that's Visionary's,
Order Book Sniper's, and Whisperer's job. Its only mandate is to watch
everything cheaply and, the instant something looks abnormal for a symbol,
fire a `RadarAlertEvent` onto `Channels.RADAR_ALERTS` so the Oracle Hub can
wake the heavier (and more expensive — some call out to LLMs) agents for
that specific symbol instead of every agent polling hundreds of symbols
itself.

Detectors implemented here:
    1. Volume spike       — a closed candle's volume vs. a rolling average
                             of the preceding N candles.
    2. RSI extreme         — Wilder's RSI(period) crossing overbought/
                             oversold thresholds.
    3. Liquidity anomaly   — top-of-book bid/ask volume imbalance deviating
                             sharply (z-score) from its own rolling
                             baseline. This is a coarse pre-screen only;
                             distinguishing a genuine imbalance from a
                             spoofed wall is the Order Book Sniper's job —
                             Radar Scout just flags "look here."

Performance note: with potentially hundreds of symbols on the watchlist,
every per-event computation here is deliberately O(1) (Wilder's RSI is
incremental; volume/imbalance baselines use small fixed-size rolling
windows) rather than recomputing over a growing history on each update.

Candle-closure handling: `CCXTFeed` streams every intra-bar update with
`is_closed=False` (true closure detection is `candle_aggregator`'s job in a
later phase). Until that lands, RadarScout finalizes bars itself: it
buffers the latest update per symbol and only feeds its indicators once a
NEW bar's timestamp arrives — at that point the previous bar is known to be
complete.
"""

from __future__ import annotations

import logging
from collections import deque
from dataclasses import dataclass, field

from pydantic import BaseModel

from agents.base_agent import BaseAgent
from core.event_bus.redis_bus import Channels, RedisEventBus
from core.event_bus.schemas import (
    OHLCVEvent,
    OrderBookEvent,
    RadarAlertEvent,
    RadarAlertType,
    TickEvent,
)

logger = logging.getLogger(__name__)


@dataclass
class _VolumeTracker:
    """Fixed-size rolling window of candle volumes for one symbol."""

    maxlen: int
    history: deque[float] = field(init=False)

    def __post_init__(self) -> None:
        self.history = deque(maxlen=self.maxlen)

    @property
    def is_warm(self) -> bool:
        """True once we have a full window — avoids flagging false spikes
        during the first few candles after startup."""
        return len(self.history) >= self.maxlen

    def rolling_average(self) -> float:
        return sum(self.history) / len(self.history) if self.history else 0.0

    def push(self, volume: float) -> None:
        self.history.append(volume)


@dataclass
class _RSITracker:
    """
    Incremental Wilder's RSI for one symbol. O(1) per update — no need to
    keep the full price history around, which matters when this is
    replicated across hundreds of symbols.
    """

    period: int
    _avg_gain: float = 0.0
    _avg_loss: float = 0.0
    _prev_close: float | None = None
    _count: int = 0

    @property
    def is_warm(self) -> bool:
        return self._count > self.period

    def push(self, close: float) -> float | None:
        """Feed one new closed-candle close price. Returns the current RSI
        once enough history has accumulated (period + 1 closes), else None."""
        if self._prev_close is None:
            self._prev_close = close
            self._count = 1
            return None

        change = close - self._prev_close
        gain = max(change, 0.0)
        loss = max(-change, 0.0)
        self._prev_close = close
        self._count += 1

        if self._count <= self.period + 1:
            # Seed phase: Wilder's method seeds avg_gain/avg_loss with a
            # plain average of the first `period` changes.
            self._avg_gain += gain / self.period
            self._avg_loss += loss / self.period
            if self._count < self.period + 1:
                return None
        else:
            # Steady-state Wilder smoothing.
            self._avg_gain = (self._avg_gain * (self.period - 1) + gain) / self.period
            self._avg_loss = (self._avg_loss * (self.period - 1) + loss) / self.period

        if self._avg_loss == 0:
            return 100.0
        relative_strength = self._avg_gain / self._avg_loss
        return 100.0 - (100.0 / (1.0 + relative_strength))


@dataclass
class _ImbalanceTracker:
    """Rolling baseline (mean/std) of order book bid/ask imbalance for one
    symbol, used to z-score the current imbalance against 'normal' for that
    specific symbol rather than a fixed global threshold."""

    maxlen: int
    history: deque[float] = field(init=False)

    def __post_init__(self) -> None:
        self.history = deque(maxlen=self.maxlen)

    @property
    def is_warm(self) -> bool:
        return len(self.history) >= self.maxlen

    def baseline_mean_std(self) -> tuple[float, float]:
        n = len(self.history)
        mean = sum(self.history) / n
        variance = sum((x - mean) ** 2 for x in self.history) / n
        return mean, variance**0.5

    def push(self, value: float) -> None:
        self.history.append(value)


class RadarScout(BaseAgent):
    """
    See module docstring for the full detector rundown. Wire this up with a
    connected `RedisEventBus` and a symbol list, `await radar.start()`, and
    it will publish `RadarAlertEvent`s to `Channels.RADAR_ALERTS` whenever
    a detector fires for any symbol it watches.
    """

    def __init__(
        self,
        event_bus: RedisEventBus,
        symbols: list[str],
        timeframe: str = "1m",
        volume_window: int = 20,
        volume_spike_multiplier: float = 3.0,
        rsi_period: int = 14,
        rsi_overbought: float = 70.0,
        rsi_oversold: float = 30.0,
        orderbook_imbalance_window: int = 30,
        orderbook_imbalance_z_threshold: float = 3.0,
    ) -> None:
        super().__init__(event_bus=event_bus)
        self.symbols = symbols
        self.timeframe = timeframe
        self._volume_spike_multiplier = volume_spike_multiplier
        self._rsi_overbought = rsi_overbought
        self._rsi_oversold = rsi_oversold
        self._orderbook_z_threshold = orderbook_imbalance_z_threshold

        self._volume_trackers = {s: _VolumeTracker(maxlen=volume_window) for s in symbols}
        self._rsi_trackers = {s: _RSITracker(period=rsi_period) for s in symbols}
        self._imbalance_trackers = {
            s: _ImbalanceTracker(maxlen=orderbook_imbalance_window) for s in symbols
        }
        # Latest not-yet-confirmed-closed candle per symbol, keyed by symbol.
        self._pending_candle: dict[str, OHLCVEvent] = {}

    @property
    def name(self) -> str:
        return "radar_scout"

    @property
    def input_channels(self) -> list[str]:
        return [Channels.ohlcv(s, self.timeframe) for s in self.symbols] + [
            Channels.orderbook(s) for s in self.symbols
        ]

    async def analyze(self, event: BaseModel) -> None:
        if isinstance(event, OHLCVEvent):
            await self._handle_ohlcv(event)
        elif isinstance(event, OrderBookEvent):
            await self._handle_orderbook(event)
        elif isinstance(event, TickEvent):
            # Deliberately ignored: screening runs off closed candles and
            # book snapshots, not every raw trade print, to keep per-event
            # cost low across a wide watchlist.
            return

    # ------------------------------------------------------------------
    # Candle finalization
    # ------------------------------------------------------------------

    async def _handle_ohlcv(self, event: OHLCVEvent) -> None:
        pending = self._pending_candle.get(event.symbol)
        if pending is not None and pending.timestamp_ms != event.timestamp_ms:
            # A new bar has started -> the previous one is now final.
            await self._finalize_candle(pending)
        self._pending_candle[event.symbol] = event

    async def _finalize_candle(self, candle: OHLCVEvent) -> None:
        await self._check_volume_spike(candle)
        await self._check_rsi_extreme(candle)

    # ------------------------------------------------------------------
    # Detector 1: volume spike
    # ------------------------------------------------------------------

    async def _check_volume_spike(self, candle: OHLCVEvent) -> None:
        tracker = self._volume_trackers[candle.symbol]
        if tracker.is_warm:
            avg = tracker.rolling_average()
            if avg > 0:
                ratio = candle.volume / avg
                if ratio >= self._volume_spike_multiplier:
                    severity = min(
                        1.0,
                        0.5 + (ratio - self._volume_spike_multiplier)
                        / self._volume_spike_multiplier,
                    )
                    await self._emit_alert(
                        symbol=candle.symbol,
                        timestamp_ms=candle.timestamp_ms,
                        alert_type=RadarAlertType.VOLUME_SPIKE,
                        severity=severity,
                        message=(
                            f"{candle.symbol}: volume {candle.volume:.2f} is {ratio:.1f}x "
                            f"the {len(tracker.history)}-bar average ({avg:.2f}) on "
                            f"{self.timeframe}."
                        ),
                        details={"volume": candle.volume, "avg_volume": avg, "ratio": ratio},
                    )
        tracker.push(candle.volume)

    # ------------------------------------------------------------------
    # Detector 2: RSI extreme
    # ------------------------------------------------------------------

    async def _check_rsi_extreme(self, candle: OHLCVEvent) -> None:
        rsi_tracker = self._rsi_trackers[candle.symbol]
        rsi = rsi_tracker.push(candle.close)
        if rsi is None:
            return

        if rsi >= self._rsi_overbought:
            severity = max(0.1, min(1.0, (rsi - self._rsi_overbought) / (100 - self._rsi_overbought)))
            await self._emit_alert(
                symbol=candle.symbol,
                timestamp_ms=candle.timestamp_ms,
                alert_type=RadarAlertType.RSI_OVERBOUGHT,
                severity=severity,
                message=(
                    f"{candle.symbol}: RSI({rsi_tracker.period}) = {rsi:.1f}, "
                    f"overbought on {self.timeframe}."
                ),
                details={"rsi": rsi},
            )
        elif rsi <= self._rsi_oversold:
            severity = max(0.1, min(1.0, (self._rsi_oversold - rsi) / self._rsi_oversold))
            await self._emit_alert(
                symbol=candle.symbol,
                timestamp_ms=candle.timestamp_ms,
                alert_type=RadarAlertType.RSI_OVERSOLD,
                severity=severity,
                message=(
                    f"{candle.symbol}: RSI({rsi_tracker.period}) = {rsi:.1f}, "
                    f"oversold on {self.timeframe}."
                ),
                details={"rsi": rsi},
            )

    # ------------------------------------------------------------------
    # Detector 3: liquidity anomaly (coarse order book imbalance)
    # ------------------------------------------------------------------

    async def _handle_orderbook(self, event: OrderBookEvent) -> None:
        if not event.bids or not event.asks:
            return

        bid_volume = sum(level.amount for level in event.bids)
        ask_volume = sum(level.amount for level in event.asks)
        total = bid_volume + ask_volume
        if total <= 0:
            return

        imbalance = (bid_volume - ask_volume) / total  # in [-1, 1]
        tracker = self._imbalance_trackers[event.symbol]

        if tracker.is_warm:
            mean, std = tracker.baseline_mean_std()
            if std > 1e-9:
                z_score = (imbalance - mean) / std
                if abs(z_score) >= self._orderbook_z_threshold:
                    severity = min(1.0, abs(z_score) / (self._orderbook_z_threshold * 2))
                    direction = "bid-heavy" if imbalance > mean else "ask-heavy"
                    await self._emit_alert(
                        symbol=event.symbol,
                        timestamp_ms=event.timestamp_ms,
                        alert_type=RadarAlertType.LIQUIDITY_ANOMALY,
                        severity=max(0.1, severity),
                        message=(
                            f"{event.symbol}: order book imbalance {imbalance:+.2f} is "
                            f"{z_score:+.1f} std devs from baseline ({direction})."
                        ),
                        details={
                            "imbalance": imbalance,
                            "z_score": z_score,
                            "baseline_mean": mean,
                        },
                    )
        tracker.push(imbalance)

    # ------------------------------------------------------------------
    # Shared alert emission
    # ------------------------------------------------------------------

    async def _emit_alert(
        self,
        symbol: str,
        timestamp_ms: int,
        alert_type: RadarAlertType,
        severity: float,
        message: str,
        details: dict[str, float],
    ) -> None:
        alert = RadarAlertEvent(
            source=self.name,
            symbol=symbol,
            timestamp_ms=timestamp_ms,
            alert_type=alert_type,
            severity=round(severity, 3),
            message=message,
            details=details,
        )
        logger.info("RADAR ALERT [%s] %s", alert_type.value, message)
        await self.publish(Channels.RADAR_ALERTS, alert)
