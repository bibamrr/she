from __future__ import annotations

from typing import Any


def _clip(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def coil_confidence(streak: int, tightness: float, quietness: float) -> dict[str, float]:
    """Score silent compression quality before any spring fires (50–92)."""
    streak_pts = _clip(4.0 * (streak**0.85), 0, 22)
    tight_pts = _clip(tightness, 0, 1) * 18.0
    quiet_pts = _clip(quietness, 0, 1) * 12.0
    total = _clip(50.0 + streak_pts + tight_pts + quiet_pts, 50.0, 92.0)
    return {
        "streak_pts": round(streak_pts, 2),
        "tightness_pts": round(tight_pts, 2),
        "quietness_pts": round(quiet_pts, 2),
        "body_pts": 0.0,
        "volume_pts": 0.0,
        "total": round(total, 1),
    }


def spring_confidence(
    streak: int,
    tightness: float,
    body_ratio: float,
    volume_ratio: float,
    close_position: float = 0.5,
    expansion: float = 1.0,
) -> dict[str, float]:
    """Score a spring breakout (50.0–95.0).

    Beyond coil length, range coil, body and volume, two follow-through factors
    separate the winners: where the bar closed inside its own range
    (``close_position``) and whether the range genuinely expanded out of the coil
    (``expansion``, penalised when the bar is an exhaustion candle).
    """
    streak_pts = _clip(2.8 * (streak**0.85), 0, 16)
    tight_pts = _clip(tightness, 0, 1) * 8.0
    if body_ratio >= 0.7:
        body_pts = 14.0
    elif body_ratio >= 0.55:
        body_pts = 10.0
    elif body_ratio >= 0.4:
        body_pts = 5.0
    else:
        body_pts = 1.0
    if volume_ratio >= 3.0:
        volume_pts = 16.0
    elif volume_ratio >= 2.2:
        volume_pts = 13.0
    elif volume_ratio >= 1.6:
        volume_pts = 9.0
    elif volume_ratio >= 1.2:
        volume_pts = 5.0
    elif volume_ratio >= 1.0:
        volume_pts = 2.0
    else:
        volume_pts = 0.0
    close_pts = _clip(close_position, 0, 1) * 10.0
    if expansion >= 3.5:
        expansion_pts = -4.0  # exhaustion bar: chasing it is where springs fail
    elif expansion >= 1.4:
        expansion_pts = _clip((expansion - 1.4) / 1.6, 0, 1) * 8.0
    else:
        expansion_pts = 0.0
    total = _clip(
        40.0 + streak_pts + tight_pts + body_pts + volume_pts + close_pts + expansion_pts,
        50.0,
        95.0,
    )
    return {
        "streak_pts": round(streak_pts, 2),
        "tightness_pts": round(tight_pts, 2),
        "quietness_pts": 0.0,
        "body_pts": round(body_pts, 2),
        "volume_pts": round(volume_pts, 2),
        "close_pts": round(close_pts, 2),
        "expansion_pts": round(expansion_pts, 2),
        "total": round(total, 1),
    }


def format_confidence(score: float) -> str:
    return f"{score:.1f}%"
