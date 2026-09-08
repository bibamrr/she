from __future__ import annotations

import pandas as pd

from indicators.momentum import ema
from indicators.volatility import atr


def sma(series: pd.Series, period: int) -> pd.Series:
    return series.rolling(period).mean()


def stochastic(df: pd.DataFrame, period: int = 14, smooth: int = 3) -> pd.DataFrame:
    lowest = df["low"].rolling(period).min()
    highest = df["high"].rolling(period).max()
    k = 100 * (df["close"] - lowest) / (highest - lowest).replace(0, 1e-12)
    d = k.rolling(smooth).mean()
    return pd.DataFrame({"k": k, "d": d})


def williams_r(df: pd.DataFrame, period: int = 14) -> pd.Series:
    highest = df["high"].rolling(period).max()
    lowest = df["low"].rolling(period).min()
    return -100 * (highest - df["close"]) / (highest - lowest).replace(0, 1e-12)


def cci(df: pd.DataFrame, period: int = 20) -> pd.Series:
    tp = (df["high"] + df["low"] + df["close"]) / 3
    ma = tp.rolling(period).mean()
    mad = tp.rolling(period).apply(lambda x: (x - x.mean()).abs().mean(), raw=True)
    return (tp - ma) / (0.015 * mad.replace(0, 1e-12))


def obv(df: pd.DataFrame) -> pd.Series:
    direction = df["close"].diff().fillna(0).apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    return (direction * df["volume"]).cumsum()


def vwap(df: pd.DataFrame) -> pd.Series:
    typical = (df["high"] + df["low"] + df["close"]) / 3
    cum_pv = (typical * df["volume"]).cumsum()
    cum_v = df["volume"].cumsum().replace(0, 1e-12)
    return cum_pv / cum_v


def donchian(df: pd.DataFrame, period: int = 20) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "upper": df["high"].rolling(period).max(),
            "lower": df["low"].rolling(period).min(),
            "mid": (df["high"].rolling(period).max() + df["low"].rolling(period).min()) / 2,
        }
    )


def keltner(df: pd.DataFrame, period: int = 20, multiplier: float = 2.0) -> pd.DataFrame:
    mid = ema(df["close"], period)
    width = atr(df, 14) * multiplier
    return pd.DataFrame({"mid": mid, "upper": mid + width, "lower": mid - width})


def supertrend(df: pd.DataFrame, period: int = 10, multiplier: float = 3.0) -> pd.Series:
    atr_s = atr(df, period)
    hl2 = (df["high"] + df["low"]) / 2
    upper = hl2 + multiplier * atr_s
    lower = hl2 - multiplier * atr_s
    st = pd.Series(index=df.index, dtype=float)
    direction = 1
    prev = lower.iloc[period] if len(df) > period else hl2.iloc[0]
    for i in range(len(df)):
        if i < period:
            st.iloc[i] = float("nan")
            continue
        if df["close"].iloc[i] > prev:
            direction = 1
        elif df["close"].iloc[i] < prev:
            direction = -1
        prev = lower.iloc[i] if direction == 1 else upper.iloc[i]
        st.iloc[i] = prev
    return st


def ichimoku(df: pd.DataFrame) -> pd.DataFrame:
    tenkan = (df["high"].rolling(9).max() + df["low"].rolling(9).min()) / 2
    kijun = (df["high"].rolling(26).max() + df["low"].rolling(26).min()) / 2
    span_a = (tenkan + kijun) / 2
    span_b = (df["high"].rolling(52).max() + df["low"].rolling(52).min()) / 2
    return pd.DataFrame({"tenkan": tenkan, "kijun": kijun, "span_a": span_a, "span_b": span_b})
