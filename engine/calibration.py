"""Continuous threshold calibration for VRCS confidence.

The engine replays historic springs across several symbols and timeframes, then
compares the confidence the model printed against what price actually did. The
output is a reliability curve plus a suggested alert threshold and a confidence
offset that pulls printed scores toward realised win rates.
"""

from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BUCKETS = ((50, 65), (65, 75), (75, 85), (85, 90), (90, 101))
MIN_BUCKET_SAMPLE = 4

PROFILE_PATH = Path("data/calibration.json")
_profile_lock = threading.Lock()
_profile_cache: dict[str, Any] = {"mtime": None, "data": None}


def _bucket_label(low: int, high: int) -> str:
    return f"{low}-{high - 1}"


def reliability(trades: list[dict[str, Any]]) -> dict[str, Any]:
    """Realised win rate per confidence bucket (the calibration curve)."""
    closed = [t for t in trades if t["outcome"] in {"win", "loss"}]
    rows: list[dict[str, Any]] = []
    for low, high in BUCKETS:
        subset = [t for t in closed if low <= t["confidence"] < high]
        wins = [t for t in subset if t["outcome"] == "win"]
        realised = round(len(wins) / len(subset) * 100, 1) if subset else None
        midpoint = (low + high - 1) / 2
        rows.append(
            {
                "bucket": _bucket_label(low, high),
                "printed_confidence": midpoint,
                "realised_win_rate": realised,
                "trades": len(subset),
                "gap": None if realised is None else round(realised - midpoint, 1),
                "avg_pnl_pct": round(sum(t["pnl_pct"] for t in subset) / len(subset), 3) if subset else None,
            }
        )
    return {"curve": rows, "closed": len(closed)}


def calibrate(reports: list[dict[str, Any]]) -> dict[str, Any]:
    """Fold several backtest reports into one calibration verdict."""
    trades: list[dict[str, Any]] = []
    for report in reports:
        for trade in report.get("trades", []):
            enriched = dict(trade)
            enriched["symbol"] = report.get("symbol")
            enriched["timeframe"] = report.get("timeframe")
            trades.append(enriched)

    curve = reliability(trades)
    rows = [r for r in curve["curve"] if r["trades"] >= 4 and r["realised_win_rate"] is not None]

    weighted_gap = 0.0
    weight_total = 0
    for row in rows:
        weighted_gap += row["gap"] * row["trades"]
        weight_total += row["trades"]
    offset = round(weighted_gap / weight_total, 1) if weight_total else 0.0

    # the alert threshold is the lowest bucket whose realised win rate still clears 50%
    suggested_threshold = 90.0
    for row in rows:
        if row["realised_win_rate"] >= 50.0:
            suggested_threshold = float(row["bucket"].split("-")[0])
            break

    elite = [t for t in trades if t["confidence"] >= 90 and t["outcome"] in {"win", "loss"}]
    elite_wins = [t for t in elite if t["outcome"] == "win"]
    elite_rate = round(len(elite_wins) / len(elite) * 100, 1) if elite else None

    per_symbol: dict[str, dict[str, Any]] = {}
    for report in reports:
        key = f"{report.get('symbol')} {report.get('timeframe')}"
        per_symbol[key] = {
            "win_rate": report.get("win_rate"),
            "signals": report.get("total_signals"),
            "closed": report.get("closed"),
            "avg_pnl_pct": report.get("avg_pnl_pct"),
        }

    monotonic = all(
        rows[i]["realised_win_rate"] <= rows[i + 1]["realised_win_rate"] for i in range(len(rows) - 1)
    ) if len(rows) > 1 else True

    return {
        "samples": len(trades),
        "closed": curve["closed"],
        "curve": curve["curve"],
        "confidence_offset": offset,
        "suggested_alert_threshold": suggested_threshold,
        "elite_win_rate": elite_rate,
        "monotonic": monotonic,
        "per_market": per_symbol,
        "verdict": _verdict(offset, elite_rate, monotonic),
    }


def save_profile(result: dict[str, Any]) -> dict[str, Any]:
    """Persist the calibration curve so live signals can be mapped through it."""
    profile = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "samples": result.get("samples"),
        "confidence_offset": result.get("confidence_offset"),
        "suggested_alert_threshold": result.get("suggested_alert_threshold"),
        "verdict": result.get("verdict"),
        "points": [
            {"printed": row["printed_confidence"], "realised": row["realised_win_rate"], "trades": row["trades"]}
            for row in result.get("curve", [])
            if row.get("realised_win_rate") is not None and row.get("trades", 0) >= MIN_BUCKET_SAMPLE
        ],
    }
    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROFILE_PATH.write_text(json.dumps(profile, ensure_ascii=False, indent=2))
    with _profile_lock:
        _profile_cache["mtime"] = PROFILE_PATH.stat().st_mtime
        _profile_cache["data"] = profile
    return profile


def load_profile() -> dict[str, Any] | None:
    if not PROFILE_PATH.exists():
        return None
    mtime = PROFILE_PATH.stat().st_mtime
    with _profile_lock:
        if _profile_cache["mtime"] == mtime:
            return _profile_cache["data"]
    try:
        profile = json.loads(PROFILE_PATH.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    with _profile_lock:
        _profile_cache["mtime"] = mtime
        _profile_cache["data"] = profile
    return profile


def calibrated_confidence(score: float) -> float | None:
    """Map a printed VRCS score onto the realised win rate measured for its bucket."""
    profile = load_profile()
    if not profile:
        return None
    points = sorted(profile.get("points", []), key=lambda p: p["printed"])
    if not points:
        return None
    if score <= points[0]["printed"]:
        return round(float(points[0]["realised"]), 1)
    if score >= points[-1]["printed"]:
        return round(float(points[-1]["realised"]), 1)
    for left, right in zip(points, points[1:]):
        if left["printed"] <= score <= right["printed"]:
            span = right["printed"] - left["printed"]
            if span <= 0:
                return round(float(left["realised"]), 1)
            ratio = (score - left["printed"]) / span
            value = left["realised"] + (right["realised"] - left["realised"]) * ratio
            return round(float(value), 1)
    return None


def _verdict(offset: float, elite_rate: float | None, monotonic: bool) -> str:
    if elite_rate is None:
        return "insufficient-elite-sample"
    if offset <= -10:
        return "over-confident"
    if offset >= 10:
        return "under-confident"
    if not monotonic:
        return "non-monotonic"
    return "calibrated"
