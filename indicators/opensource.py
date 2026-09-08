"""Open-source technical indicators re-implemented on pandas.

Every function here is a from-formula implementation of a publicly documented
indicator (Wilder, Lambert, Elder, LazyBear's squeeze/wave-trend, etc.) so the
whole popular open-source toolkit is available next to SHC VRCS.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from indicators.momentum import ema
from indicators.volatility import true_range


# ----------------------------------------------------------------- averages

def wma(series: pd.Series, period: int) -> pd.Series:
    weights = np.arange(1, period + 1)
    return series.rolling(period).apply(lambda w: np.dot(w, weights) / weights.sum(), raw=True)


def hma(series: pd.Series, period: int = 21) -> pd.Series:
    """Hull moving average — faster and smoother than a plain WMA."""
    half = max(1, period // 2)
    sqrt_len = max(1, int(round(period**0.5)))
    return wma(2 * wma(series, half) - wma(series, period), sqrt_len)


def dema(series: pd.Series, period: int = 21) -> pd.Series:
    first = ema(series, period)
    return 2 * first - ema(first, period)


def tema(series: pd.Series, period: int = 21) -> pd.Series:
    e1 = ema(series, period)
    e2 = ema(e1, period)
    e3 = ema(e2, period)
    return 3 * e1 - 3 * e2 + e3


def zlema(series: pd.Series, period: int = 21) -> pd.Series:
    lag = (period - 1) // 2
    return ema(series + (series - series.shift(lag)), period)


def vwma(df: pd.DataFrame, period: int = 20) -> pd.Series:
    pv = (df["close"] * df["volume"]).rolling(period).sum()
    vol = df["volume"].rolling(period).sum()
    return pv / vol.replace(0, np.nan)


# ----------------------------------------------------------------- momentum

def roc(series: pd.Series, period: int = 12) -> pd.Series:
    return (series / series.shift(period) - 1) * 100


def momentum(series: pd.Series, period: int = 10) -> pd.Series:
    return series - series.shift(period)


def trix(series: pd.Series, period: int = 15) -> pd.Series:
    smoothed = ema(ema(ema(series, period), period), period)
    return smoothed.pct_change() * 100


def ppo(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> dict[str, pd.Series]:
    line = (ema(series, fast) - ema(series, slow)) / ema(series, slow) * 100
    sig = ema(line, signal)
    return {"ppo": line, "ppo_signal": sig, "ppo_hist": line - sig}


def awesome_oscillator(df: pd.DataFrame, fast: int = 5, slow: int = 34) -> pd.Series:
    median = (df["high"] + df["low"]) / 2
    return median.rolling(fast).mean() - median.rolling(slow).mean()


def ultimate_oscillator(df: pd.DataFrame, short: int = 7, medium: int = 14, long: int = 28) -> pd.Series:
    prior_close = df["close"].shift(1)
    true_low = pd.concat([df["low"], prior_close], axis=1).min(axis=1)
    buying_pressure = df["close"] - true_low
    tr = true_range(df)

    def avg(period: int) -> pd.Series:
        return buying_pressure.rolling(period).sum() / tr.rolling(period).sum().replace(0, np.nan)

    return 100 * (4 * avg(short) + 2 * avg(medium) + avg(long)) / 7


def coppock(series: pd.Series, long: int = 14, short: int = 11, smooth: int = 10) -> pd.Series:
    return wma(roc(series, long) + roc(series, short), smooth)


def kst(series: pd.Series) -> dict[str, pd.Series]:
    parts = [(10, 10), (15, 10), (20, 10), (30, 15)]
    weights = [1, 2, 3, 4]
    total = None
    for (rate, smooth), weight in zip(parts, weights):
        piece = roc(series, rate).rolling(smooth).mean() * weight
        total = piece if total is None else total + piece
    line = total
    return {"kst": line, "kst_signal": line.rolling(9).mean()}


def fisher_transform(df: pd.DataFrame, period: int = 9) -> pd.Series:
    median = (df["high"] + df["low"]) / 2
    lowest = median.rolling(period).min()
    highest = median.rolling(period).max()
    span = (highest - lowest).replace(0, np.nan)
    normalized = (2 * ((median - lowest) / span) - 1).fillna(0.0)
    smoothed = normalized.ewm(alpha=0.33, adjust=False).mean().clip(-0.999, 0.999)
    return 0.5 * np.log((1 + smoothed) / (1 - smoothed))


def wave_trend(df: pd.DataFrame, channel: int = 10, average: int = 21) -> dict[str, pd.Series]:
    """LazyBear's WaveTrend oscillator."""
    typical = (df["high"] + df["low"] + df["close"]) / 3
    esa = ema(typical, channel)
    deviation = ema((typical - esa).abs(), channel)
    ci = (typical - esa) / (0.015 * deviation.replace(0, np.nan))
    wt1 = ema(ci, average)
    wt2 = wt1.rolling(4).mean()
    return {"wt1": wt1, "wt2": wt2}


# ---------------------------------------------------------------- direction

def adx(df: pd.DataFrame, period: int = 14) -> dict[str, pd.Series]:
    """Wilder's ADX with the +DI / -DI pair."""
    up = df["high"].diff()
    down = -df["low"].diff()
    plus_dm = up.where((up > down) & (up > 0), 0.0)
    minus_dm = down.where((down > up) & (down > 0), 0.0)
    atr_w = true_range(df).ewm(alpha=1 / period, adjust=False).mean()
    plus_di = 100 * plus_dm.ewm(alpha=1 / period, adjust=False).mean() / atr_w.replace(0, np.nan)
    minus_di = 100 * minus_dm.ewm(alpha=1 / period, adjust=False).mean() / atr_w.replace(0, np.nan)
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    return {"adx": dx.ewm(alpha=1 / period, adjust=False).mean(), "plus_di": plus_di, "minus_di": minus_di}


def aroon(df: pd.DataFrame, period: int = 25) -> dict[str, pd.Series]:
    up = df["high"].rolling(period + 1).apply(lambda w: float(np.argmax(w)) / period * 100, raw=True)
    down = df["low"].rolling(period + 1).apply(lambda w: float(np.argmin(w)) / period * 100, raw=True)
    return {"aroon_up": up, "aroon_down": down, "aroon_osc": up - down}


def parabolic_sar(df: pd.DataFrame, step: float = 0.02, cap: float = 0.2) -> pd.Series:
    high = df["high"].to_numpy(dtype=float)
    low = df["low"].to_numpy(dtype=float)
    length = len(df)
    sar = np.full(length, np.nan)
    if length < 3:
        return pd.Series(sar, index=df.index)

    rising = high[1] >= high[0]
    acceleration = step
    extreme = high[0] if rising else low[0]
    sar[0] = low[0] if rising else high[0]

    for i in range(1, length):
        prior = sar[i - 1]
        value = prior + acceleration * (extreme - prior)
        if rising:
            value = min(value, low[i - 1], low[max(i - 2, 0)])
            if low[i] < value:
                rising = False
                value = extreme
                extreme = low[i]
                acceleration = step
            elif high[i] > extreme:
                extreme = high[i]
                acceleration = min(acceleration + step, cap)
        else:
            value = max(value, high[i - 1], high[max(i - 2, 0)])
            if high[i] > value:
                rising = True
                value = extreme
                extreme = high[i]
                acceleration = step
            elif low[i] < extreme:
                extreme = low[i]
                acceleration = min(acceleration + step, cap)
        sar[i] = value
    return pd.Series(sar, index=df.index)


def vortex(df: pd.DataFrame, period: int = 14) -> dict[str, pd.Series]:
    vm_plus = (df["high"] - df["low"].shift(1)).abs().rolling(period).sum()
    vm_minus = (df["low"] - df["high"].shift(1)).abs().rolling(period).sum()
    tr_sum = true_range(df).rolling(period).sum().replace(0, np.nan)
    return {"vi_plus": vm_plus / tr_sum, "vi_minus": vm_minus / tr_sum}


def chandelier_exit(df: pd.DataFrame, period: int = 22, multiplier: float = 3.0) -> dict[str, pd.Series]:
    atr_v = true_range(df).rolling(period).mean()
    return {
        "chandelier_long": df["high"].rolling(period).max() - atr_v * multiplier,
        "chandelier_short": df["low"].rolling(period).min() + atr_v * multiplier,
    }


def elder_ray(df: pd.DataFrame, period: int = 13) -> dict[str, pd.Series]:
    base = ema(df["close"], period)
    return {"bull_power": df["high"] - base, "bear_power": df["low"] - base}


# ------------------------------------------------------- volume & pressure

def mfi(df: pd.DataFrame, period: int = 14) -> pd.Series:
    typical = (df["high"] + df["low"] + df["close"]) / 3
    flow = typical * df["volume"]
    delta = typical.diff()
    positive = flow.where(delta > 0, 0.0).rolling(period).sum()
    negative = flow.where(delta < 0, 0.0).rolling(period).sum()
    ratio = positive / negative.replace(0, np.nan)
    return 100 - (100 / (1 + ratio))


def chaikin_money_flow(df: pd.DataFrame, period: int = 20) -> pd.Series:
    span = (df["high"] - df["low"]).replace(0, np.nan)
    multiplier = ((df["close"] - df["low"]) - (df["high"] - df["close"])) / span
    money_flow = multiplier * df["volume"]
    return money_flow.rolling(period).sum() / df["volume"].rolling(period).sum().replace(0, np.nan)


def accumulation_distribution(df: pd.DataFrame) -> pd.Series:
    span = (df["high"] - df["low"]).replace(0, np.nan)
    multiplier = ((df["close"] - df["low"]) - (df["high"] - df["close"])) / span
    return (multiplier.fillna(0.0) * df["volume"]).cumsum()


def chaikin_oscillator(df: pd.DataFrame, fast: int = 3, slow: int = 10) -> pd.Series:
    line = accumulation_distribution(df)
    return ema(line, fast) - ema(line, slow)


def force_index(df: pd.DataFrame, period: int = 13) -> pd.Series:
    return ema(df["close"].diff() * df["volume"], period)


def ease_of_movement(df: pd.DataFrame, period: int = 14) -> pd.Series:
    distance = ((df["high"] + df["low"]) / 2).diff()
    box = (df["volume"] / 1_000_000) / (df["high"] - df["low"]).replace(0, np.nan)
    return (distance / box.replace(0, np.nan)).rolling(period).mean()


# -------------------------------------------------------------- volatility

def bollinger_extras(series: pd.Series, period: int = 20, deviations: float = 2.0) -> dict[str, pd.Series]:
    mid = series.rolling(period).mean()
    sd = series.rolling(period).std(ddof=0)
    upper = mid + sd * deviations
    lower = mid - sd * deviations
    width = (upper - lower) / mid.replace(0, np.nan) * 100
    percent_b = (series - lower) / (upper - lower).replace(0, np.nan) * 100
    return {"bb_percent_b": percent_b, "bb_bandwidth": width}


def squeeze_momentum(df: pd.DataFrame, period: int = 20, bb_mult: float = 2.0, kc_mult: float = 1.5) -> dict[str, pd.Series]:
    """LazyBear's squeeze momentum: Bollinger inside Keltner marks the coil."""
    close = df["close"]
    basis = close.rolling(period).mean()
    sd = close.rolling(period).std(ddof=0)
    bb_upper, bb_lower = basis + bb_mult * sd, basis - bb_mult * sd
    range_ma = true_range(df).rolling(period).mean()
    kc_upper, kc_lower = basis + kc_mult * range_ma, basis - kc_mult * range_ma

    highest = df["high"].rolling(period).max()
    lowest = df["low"].rolling(period).min()
    reference = (highest + lowest) / 2
    detrended = close - (reference + basis) / 2
    slope = detrended.rolling(period).apply(
        lambda w: np.polyfit(np.arange(len(w)), w, 1)[0] * (len(w) - 1) + np.polyfit(np.arange(len(w)), w, 1)[1],
        raw=True,
    )
    squeeze_on = (bb_lower > kc_lower) & (bb_upper < kc_upper)
    return {"squeeze_momentum": slope, "squeeze_on": squeeze_on.astype(float)}


def pivot_points(df: pd.DataFrame) -> dict[str, pd.Series]:
    high = df["high"].shift(1)
    low = df["low"].shift(1)
    close = df["close"].shift(1)
    pivot = (high + low + close) / 3
    return {
        "pivot": pivot,
        "pivot_r1": 2 * pivot - low,
        "pivot_s1": 2 * pivot - high,
        "pivot_r2": pivot + (high - low),
        "pivot_s2": pivot - (high - low),
    }
