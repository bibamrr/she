from __future__ import annotations

import numpy as np

from backend.app.services.analysis import run_swarm


def _synth(n: int = 80) -> list[dict]:
    close = 100 + np.cumsum(np.linspace(-0.1, 0.15, n))
    rows = []
    ts = 1_700_000_000_000
    for i, c in enumerate(close):
        o = float(c) - 0.2
        h = float(c) + 0.4
        l = float(c) - 0.5
        rows.append(
            {
                "time": ts // 1000 + i * 60,
                "timestamp_ms": ts + i * 60_000,
                "open": o,
                "high": h,
                "low": l,
                "close": float(c),
                "volume": 10 + i,
            }
        )
    return rows


def test_swarm_returns_three_agents():
    result = run_swarm(_synth())
    assert len(result["opinions"]) == 3
    assert result["consensus"]["direction"] in {"bullish", "bearish", "neutral"}
    assert result["last_close"] > 0
