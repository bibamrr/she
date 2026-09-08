from __future__ import annotations

from typing import Any

from engine.vrcs import compute_vrcs

TF_WEIGHTS = {
    "1m": 1.0,
    "3m": 1.2,
    "5m": 1.4,
    "15m": 1.8,
    "30m": 2.0,
    "1h": 2.4,
    "2h": 2.6,
    "4h": 3.0,
    "6h": 3.1,
    "12h": 3.3,
    "1d": 3.6,
}


SIGNAL_FRESH_BARS = 5


def _verdict(vrcs: dict[str, Any], df: Any) -> dict[str, Any]:
    """Read one timeframe's VRCS state, only trusting a spring that is still fresh."""
    dash = vrcs["dashboard"]
    regime = dash["regime"]
    signals = vrcs["signals"]
    last = signals[-1] if signals else None
    bars_ago = None
    if last is not None:
        times = df["time"].tolist()
        try:
            bars_ago = len(times) - 1 - times.index(int(last["time"]))
        except ValueError:
            bars_ago = None

    side = None
    confidence = float(dash["confidence"] or 0.0)
    if regime.startswith("spring_"):
        side = regime.split("_", 1)[1]
    elif last is not None and bars_ago is not None and bars_ago <= SIGNAL_FRESH_BARS:
        side = last["side"]
        confidence = max(confidence, float(last["confidence"]))

    return {
        "regime": regime,
        "side": side,
        "confidence": round(confidence, 1),
        "streak": dash["streak"],
        "bars_since_signal": bars_ago,
        "last_signal": last,
    }


def confluence(frames: dict[str, Any]) -> dict[str, Any]:
    """Aggregate VRCS state across timeframes into one confluence verdict.

    `frames` maps timeframe -> DataFrame with time/open/high/low/close/volume.
    """
    per_tf: list[dict[str, Any]] = []
    for timeframe, df in frames.items():
        if df is None or len(df) < 40:
            continue
        vrcs = compute_vrcs(df)
        verdict = _verdict(vrcs, df)
        verdict["timeframe"] = timeframe
        verdict["weight"] = TF_WEIGHTS.get(timeframe, 1.5)
        per_tf.append(verdict)

    if not per_tf:
        return {"direction": "neutral", "score": 0.0, "confluence_confidence": 0.0, "frames": []}

    total_weight = sum(v["weight"] for v in per_tf)
    bull = sum(v["weight"] for v in per_tf if v["side"] == "bullish")
    bear = sum(v["weight"] for v in per_tf if v["side"] == "bearish")
    coiled = [v for v in per_tf if v["regime"] == "compression"]
    coil_ratio = sum(v["weight"] for v in coiled) / total_weight

    score = (bull - bear) / total_weight
    if score > 0.15:
        direction = "bullish"
    elif score < -0.15:
        direction = "bearish"
    else:
        direction = "neutral"

    agreeing = [v for v in per_tf if v["side"] == direction and direction != "neutral"]
    avg_conf = sum(v["confidence"] for v in agreeing) / len(agreeing) if agreeing else 0.0
    alignment_bonus = min(12.0, 4.0 * len(agreeing))
    coil_bonus = coil_ratio * 8.0
    confluence_confidence = round(min(97.0, avg_conf + alignment_bonus + coil_bonus), 1) if agreeing else round(
        50.0 + coil_ratio * 20.0, 1
    )

    return {
        "direction": direction,
        "score": round(score, 3),
        "aligned_frames": [v["timeframe"] for v in agreeing],
        "coiled_frames": [v["timeframe"] for v in coiled],
        "coil_ratio": round(coil_ratio, 3),
        "confluence_confidence": confluence_confidence,
        "frames": per_tf,
    }
