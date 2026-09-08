from __future__ import annotations

from typing import Any

import pandas as pd

from engine.calibration import calibrated_confidence
from engine.confidence import coil_confidence, format_confidence, spring_confidence


def _sma(series: pd.Series, period: int) -> pd.Series:
    return series.rolling(period, min_periods=period).mean()


def compute_vrcs(
    df: pd.DataFrame,
    compression_period: int = 20,
    threshold_multiplier: float = 0.6,
    volume_factor: float = 0.7,
    lookback_breakout: int = 3,
) -> dict[str, Any]:
    work = df.copy()
    work["candle_range"] = (work["high"] - work["low"]).clip(lower=1e-12)
    work["body"] = (work["close"] - work["open"]).abs()
    work["avg_range"] = _sma(work["candle_range"], compression_period)
    work["avg_volume"] = _sma(work["volume"], compression_period)

    compressed = (work["candle_range"] <= work["avg_range"] * threshold_multiplier) & (
        work["volume"] <= work["avg_volume"] * volume_factor
    )
    work["compressed"] = compressed.fillna(False)

    streak = 0
    streaks: list[int] = []
    for flag in work["compressed"].tolist():
        streak = streak + 1 if flag else 0
        streaks.append(streak)
    work["streak"] = streaks

    zones: list[dict[str, Any]] = []
    signals: list[dict[str, Any]] = []
    bar_confidence: list[float | None] = []
    lookback = max(1, lookback_breakout)

    for i in range(len(work)):
        row = work.iloc[i]
        ts = int(row["time"]) if "time" in work.columns else int(i)
        avg_range = float(row["avg_range"]) if pd.notna(row["avg_range"]) else 0.0
        avg_vol = float(row["avg_volume"]) if pd.notna(row["avg_volume"]) else 0.0
        rng = float(row["candle_range"])
        vol = float(row["volume"])
        tightness = 0.0
        quietness = 0.0
        if avg_range > 0:
            tightness = max(0.0, 1.0 - rng / (avg_range * max(threshold_multiplier, 1e-6)))
        if avg_vol > 0:
            quietness = max(0.0, 1.0 - vol / (avg_vol * max(volume_factor, 1e-6)))

        if bool(row["compressed"]):
            parts = coil_confidence(int(row["streak"]), tightness, quietness)
            zones.append({"time": ts, "streak": int(row["streak"]), "confidence": parts["total"], "parts": parts})
            bar_confidence.append(parts["total"])
            continue

        bar_confidence.append(None)
        if i < compression_period or i < lookback:
            continue
        prior_streak = int(work.iloc[i - 1]["streak"])
        if prior_streak < 1:
            continue
        window = work.iloc[i - lookback : i]
        zone_high = float(window["high"].max())
        zone_low = float(window["low"].min())
        close = float(row["close"])
        open_ = float(row["open"])
        body_ratio = float(row["body"]) / rng
        vol_ratio = (vol / avg_vol) if avg_vol > 0 else 0.0
        volume_confirmed = vol > avg_vol > 0
        prior_tight = 0.0
        if pd.notna(work.iloc[i - 1]["avg_range"]) and float(work.iloc[i - 1]["avg_range"]) > 0:
            prior_tight = max(
                0.0,
                1.0
                - float(work.iloc[i - 1]["candle_range"])
                / (float(work.iloc[i - 1]["avg_range"]) * max(threshold_multiplier, 1e-6)),
            )

        side = None
        if close > zone_high and close > open_ and volume_confirmed:
            side = "bullish"
        elif close < zone_low and close < open_ and volume_confirmed:
            side = "bearish"
        if side is None:
            continue

        high = float(row["high"])
        low = float(row["low"])
        if side == "bullish":
            close_position = (close - low) / rng
        else:
            close_position = (high - close) / rng
        expansion = (rng / avg_range) if avg_range > 0 else 1.0

        parts = spring_confidence(
            prior_streak,
            prior_tight,
            body_ratio,
            vol_ratio,
            close_position,
            expansion,
        )
        score = parts["total"]
        calibrated = calibrated_confidence(score)
        bar_confidence[i] = score
        signals.append(
            {
                "time": ts,
                "side": side,
                "confidence": score,
                "calibrated_confidence": calibrated,
                "parts": parts,
                "price": close,
                "streak": prior_streak,
                "body_ratio": round(body_ratio, 3),
                "volume_ratio": round(vol_ratio, 3),
                "close_position": round(close_position, 3),
                "expansion": round(expansion, 3),
                "label": format_confidence(score),
            }
        )

    last = work.iloc[-1]
    last_signal = signals[-1] if signals else None
    last_zone = zones[-1] if zones else None
    if bool(last["compressed"]) and last_zone:
        regime = "compression"
        regime_confidence = last_zone["confidence"]
        parts = last_zone.get("parts")
    elif last_signal and last_signal["time"] == int(last["time"]):
        regime = f"spring_{last_signal['side']}"
        regime_confidence = last_signal["confidence"]
        parts = last_signal.get("parts")
    else:
        regime = "normal"
        regime_confidence = 0.0
        parts = None

    return {
        "id": "vrcs",
        "name": "SHC VRCS",
        "compressed": [bool(x) for x in work["compressed"].tolist()],
        "bar_confidence": bar_confidence,
        "zones": zones,
        "signals": signals,
        "dashboard": {
            "regime": regime,
            "confidence": regime_confidence,
            "parts": parts,
            "streak": int(last["streak"]),
            "avg_range": None if pd.isna(last["avg_range"]) else float(last["avg_range"]),
            "avg_volume": None if pd.isna(last["avg_volume"]) else float(last["avg_volume"]),
            "last_signal": last_signal,
            "show_dashboard": True,
        },
    }
