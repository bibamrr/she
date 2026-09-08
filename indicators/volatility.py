"""
indicators/volatility.py

Volatility indicators used for dynamic stop-loss sizing. ATR (Average True
Range) is the backbone of the "dynamic SL" requirement from the original
architecture — a fixed-percentage stop makes no sense across assets with
wildly different volatility, so both `agents/visionary.py` and, later, the
Oracle Hub's risk engine derive stop distances from ATR instead.

Cross-reference: `config/settings.py`'s `RiskThresholds.
default_stop_loss_atr_multiplier` is the platform-wide default multiplier;
`atr_stop_distance()` below is the function that actually turns
"multiplier" into a real price distance for a given symbol/timeframe.
"""

from __future__ import annotations

import pandas as pd


def true_range(df: pd.DataFrame) -> pd.Series:
    """
    True Range for each row: the largest of
        - high - low (this bar's own range)
        - |high - previous close|
        - |low - previous close|

    The latter two terms capture gaps between bars, which plain high-low
    range misses — important for anything that isn't a perfectly
    continuous 24/7 market... which, admittedly, crypto mostly is, but this
    module is shared with the eventual US-equities path too, where
    overnight gaps are the norm.

    Parameters
    ----------
    df:
        DataFrame with 'high', 'low', 'close' columns, oldest row first.
    """
    prev_close = df["close"].shift(1)
    range_high_low = df["high"] - df["low"]
    range_high_prev_close = (df["high"] - prev_close).abs()
    range_low_prev_close = (df["low"] - prev_close).abs()

    return pd.concat(
        [range_high_low, range_high_prev_close, range_low_prev_close], axis=1
    ).max(axis=1)


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Average True Range: Wilder's smoothed moving average of `true_range`.

    Like `indicators.momentum.rsi`, this uses `ewm(alpha=1/period)` as the
    vectorized equivalent of Wilder's original smoothing formula.

    Parameters
    ----------
    df:
        DataFrame with 'high', 'low', 'close' columns, oldest row first.
    period:
        Lookback period, 14 by default (the conventional value).
    """
    tr = true_range(df)
    return tr.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()


def atr_stop_distance(df: pd.DataFrame, period: int = 14, multiplier: float = 1.5) -> pd.Series:
    """
    Convenience wrapper: ATR scaled by a risk multiplier, giving a
    ready-to-use stop-loss *distance* (not a price level — callers subtract
    this from entry for a long, or add it for a short).

    Returns a full Series (one distance per row) rather than a single
    scalar so callers can either take `.iloc[-1]` for "the current
    distance" or inspect how it's evolved over the window.
    """
    return atr(df, period=period) * multiplier
