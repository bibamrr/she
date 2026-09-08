from __future__ import annotations

from typing import Any

import pandas as pd

from engine.vrcs import compute_vrcs
from indicators.volatility import atr


def evaluate_signals(
    df: pd.DataFrame,
    horizon: int = 24,
    reward_multiple: float = 2.0,
    atr_period: int = 14,
    atr_multiplier: float = 1.5,
    vrcs_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Walk every VRCS spring forward `horizon` bars and score the outcome.

    A trade wins when the reward target is reached before the ATR stop.
    """
    params = vrcs_params or {}
    vrcs = compute_vrcs(
        df,
        compression_period=int(params.get("compression_period", 20)),
        threshold_multiplier=float(params.get("threshold_multiplier", 0.6)),
        volume_factor=float(params.get("volume_factor", 0.7)),
        lookback_breakout=int(params.get("lookback_breakout", 3)),
    )
    atr_series = atr(df, atr_period)
    time_index = {int(ts): i for i, ts in enumerate(df["time"].tolist())}
    trades: list[dict[str, Any]] = []

    for signal in vrcs["signals"]:
        idx = time_index.get(int(signal["time"]))
        if idx is None or idx + 2 >= len(df):
            continue
        atr_now = float(atr_series.iloc[idx]) if pd.notna(atr_series.iloc[idx]) else 0.0
        if atr_now <= 0:
            continue
        entry = float(signal["price"])
        risk = atr_now * atr_multiplier
        long_side = signal["side"] == "bullish"
        stop = entry - risk if long_side else entry + risk
        target = entry + risk * reward_multiple if long_side else entry - risk * reward_multiple

        window = df.iloc[idx + 1 : idx + 1 + horizon]
        outcome = "open"
        bars_held = len(window)
        exit_price = float(window["close"].iloc[-1]) if len(window) else entry
        for offset in range(len(window)):
            high = float(window["high"].iloc[offset])
            low = float(window["low"].iloc[offset])
            hit_target = high >= target if long_side else low <= target
            hit_stop = low <= stop if long_side else high >= stop
            if hit_target and not hit_stop:
                outcome, bars_held, exit_price = "win", offset + 1, target
                break
            if hit_stop and not hit_target:
                outcome, bars_held, exit_price = "loss", offset + 1, stop
                break
            if hit_target and hit_stop:
                outcome, bars_held, exit_price = "loss", offset + 1, stop
                break

        move_pct = ((exit_price - entry) / entry * 100) if long_side else ((entry - exit_price) / entry * 100)
        max_fav = (
            (float(window["high"].max()) - entry) / entry * 100
            if long_side and len(window)
            else (entry - float(window["low"].min())) / entry * 100
            if len(window)
            else 0.0
        )
        trades.append(
            {
                "time": int(signal["time"]),
                "side": signal["side"],
                "confidence": signal["confidence"],
                "entry": round(entry, 8),
                "stop": round(stop, 8),
                "target": round(target, 8),
                "outcome": outcome,
                "bars_held": bars_held,
                "pnl_pct": round(move_pct, 3),
                "max_favorable_pct": round(max_fav, 3),
                "streak": signal["streak"],
                "volume_ratio": signal["volume_ratio"],
            }
        )

    closed = [tr for tr in trades if tr["outcome"] in {"win", "loss"}]
    wins = [tr for tr in closed if tr["outcome"] == "win"]
    win_rate = round(len(wins) / len(closed) * 100, 1) if closed else 0.0
    high_conf = [tr for tr in closed if tr["confidence"] >= 90]
    high_conf_wr = round(
        len([tr for tr in high_conf if tr["outcome"] == "win"]) / len(high_conf) * 100, 1
    ) if high_conf else 0.0

    buckets: dict[str, dict[str, Any]] = {}
    for lo, hi in ((50, 65), (65, 80), (80, 90), (90, 101)):
        rows = [tr for tr in closed if lo <= tr["confidence"] < hi]
        w = len([tr for tr in rows if tr["outcome"] == "win"])
        buckets[f"{lo}-{hi - 1}"] = {
            "trades": len(rows),
            "win_rate": round(w / len(rows) * 100, 1) if rows else 0.0,
        }

    return {
        "trades": trades[-120:],
        "total_signals": len(trades),
        "closed": len(closed),
        "win_rate": win_rate,
        "high_confidence_win_rate": high_conf_wr,
        "avg_pnl_pct": round(sum(tr["pnl_pct"] for tr in closed) / len(closed), 3) if closed else 0.0,
        "buckets": buckets,
        "horizon": horizon,
        "reward_multiple": reward_multiple,
    }
