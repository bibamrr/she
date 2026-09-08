from __future__ import annotations

from typing import Any, Iterable

import pandas as pd

from engine.vrcs import compute_vrcs
from indicators.classic import cci, donchian, ichimoku, keltner, obv, stochastic, supertrend, vwap, williams_r
from indicators.momentum import ema, macd, rsi
from indicators.opensource import (
    accumulation_distribution,
    adx,
    aroon,
    awesome_oscillator,
    bollinger_extras,
    chaikin_money_flow,
    chaikin_oscillator,
    chandelier_exit,
    coppock,
    dema,
    ease_of_movement,
    elder_ray,
    fisher_transform,
    force_index,
    hma,
    kst,
    mfi,
    momentum,
    parabolic_sar,
    pivot_points,
    ppo,
    roc,
    squeeze_momentum,
    tema,
    trix,
    ultimate_oscillator,
    vortex,
    vwma,
    wave_trend,
    wma,
    zlema,
)
from indicators.volatility import atr


CATALOG = [
    {"id": "vrcs", "name": "SHC VRCS", "group": "shc", "pane": "overlay"},
    {"id": "sma20", "name": "SMA 20", "group": "trend", "pane": "overlay"},
    {"id": "sma50", "name": "SMA 50", "group": "trend", "pane": "overlay"},
    {"id": "sma200", "name": "SMA 200", "group": "trend", "pane": "overlay"},
    {"id": "ema12", "name": "EMA 12", "group": "trend", "pane": "overlay"},
    {"id": "ema26", "name": "EMA 26", "group": "trend", "pane": "overlay"},
    {"id": "vwap", "name": "VWAP", "group": "trend", "pane": "overlay"},
    {"id": "supertrend", "name": "Supertrend", "group": "trend", "pane": "overlay"},
    {"id": "ichimoku", "name": "Ichimoku", "group": "trend", "pane": "overlay"},
    {"id": "donchian", "name": "Donchian", "group": "volatility", "pane": "overlay"},
    {"id": "keltner", "name": "Keltner", "group": "volatility", "pane": "overlay"},
    {"id": "bb", "name": "Bollinger Bands", "group": "volatility", "pane": "overlay"},
    {"id": "atr", "name": "ATR 14", "group": "volatility", "pane": "oscillator"},
    {"id": "rsi", "name": "RSI 14", "group": "momentum", "pane": "oscillator"},
    {"id": "macd", "name": "MACD", "group": "momentum", "pane": "oscillator"},
    {"id": "stoch", "name": "Stochastic", "group": "momentum", "pane": "oscillator"},
    {"id": "willr", "name": "Williams %R", "group": "momentum", "pane": "oscillator"},
    {"id": "cci", "name": "CCI 20", "group": "momentum", "pane": "oscillator"},
    {"id": "obv", "name": "OBV", "group": "volume", "pane": "oscillator"},
    {"id": "volume", "name": "Volume", "group": "volume", "pane": "volume"},
    # open-source library
    {"id": "wma", "name": "WMA 20", "group": "trend", "pane": "overlay"},
    {"id": "hma", "name": "Hull MA 21", "group": "trend", "pane": "overlay"},
    {"id": "dema", "name": "DEMA 21", "group": "trend", "pane": "overlay"},
    {"id": "tema", "name": "TEMA 21", "group": "trend", "pane": "overlay"},
    {"id": "zlema", "name": "ZLEMA 21", "group": "trend", "pane": "overlay"},
    {"id": "vwma", "name": "VWMA 20", "group": "trend", "pane": "overlay"},
    {"id": "psar", "name": "Parabolic SAR", "group": "trend", "pane": "overlay"},
    {"id": "pivots", "name": "Pivot Points", "group": "trend", "pane": "overlay"},
    {"id": "chandelier", "name": "Chandelier Exit", "group": "volatility", "pane": "overlay"},
    {"id": "adx", "name": "ADX / DMI", "group": "direction", "pane": "oscillator"},
    {"id": "aroon", "name": "Aroon", "group": "direction", "pane": "oscillator"},
    {"id": "vortex", "name": "Vortex", "group": "direction", "pane": "oscillator"},
    {"id": "roc", "name": "Rate of Change", "group": "momentum", "pane": "oscillator"},
    {"id": "momentum", "name": "Momentum", "group": "momentum", "pane": "oscillator"},
    {"id": "trix", "name": "TRIX", "group": "momentum", "pane": "oscillator"},
    {"id": "ppo", "name": "PPO", "group": "momentum", "pane": "oscillator"},
    {"id": "ao", "name": "Awesome Oscillator", "group": "momentum", "pane": "oscillator"},
    {"id": "uo", "name": "Ultimate Oscillator", "group": "momentum", "pane": "oscillator"},
    {"id": "coppock", "name": "Coppock Curve", "group": "momentum", "pane": "oscillator"},
    {"id": "kst", "name": "KST", "group": "momentum", "pane": "oscillator"},
    {"id": "fisher", "name": "Fisher Transform", "group": "momentum", "pane": "oscillator"},
    {"id": "wavetrend", "name": "WaveTrend (LazyBear)", "group": "momentum", "pane": "oscillator"},
    {"id": "squeeze", "name": "Squeeze Momentum (LazyBear)", "group": "volatility", "pane": "oscillator"},
    {"id": "bbextras", "name": "BB %B / Bandwidth", "group": "volatility", "pane": "oscillator"},
    {"id": "elder", "name": "Elder Ray", "group": "direction", "pane": "oscillator"},
    {"id": "mfi", "name": "Money Flow Index", "group": "volume", "pane": "oscillator"},
    {"id": "cmf", "name": "Chaikin Money Flow", "group": "volume", "pane": "oscillator"},
    {"id": "adline", "name": "Accumulation / Distribution", "group": "volume", "pane": "oscillator"},
    {"id": "chaikin", "name": "Chaikin Oscillator", "group": "volume", "pane": "oscillator"},
    {"id": "fi", "name": "Force Index", "group": "volume", "pane": "oscillator"},
    {"id": "eom", "name": "Ease of Movement", "group": "volume", "pane": "oscillator"},
]


def _points(times: Iterable[int], values: pd.Series) -> list[dict[str, float]]:
    out: list[dict[str, float]] = []
    for ts, value in zip(times, values):
        if pd.isna(value):
            continue
        out.append({"time": int(ts), "value": float(value)})
    return out


def compute_pack(
    df: pd.DataFrame,
    indicator_ids: list[str],
    vrcs_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    times = df["time"].tolist()
    close = df["close"]
    overlays: dict[str, Any] = {}
    oscillators: dict[str, Any] = {}
    vrcs = None
    params = vrcs_params or {}
    wanted = set(indicator_ids) or {"vrcs", "volume"}
    wanted.add("volume")

    if "vrcs" in wanted:
        vrcs = compute_vrcs(
            df,
            compression_period=int(params.get("compression_period", 20)),
            threshold_multiplier=float(params.get("threshold_multiplier", 0.6)),
            volume_factor=float(params.get("volume_factor", 0.7)),
            lookback_breakout=int(params.get("lookback_breakout", 3)),
        )
    if "sma20" in wanted:
        overlays["sma20"] = _points(times, close.rolling(20).mean())
    if "sma50" in wanted:
        overlays["sma50"] = _points(times, close.rolling(50).mean())
    if "sma200" in wanted:
        overlays["sma200"] = _points(times, close.rolling(200).mean())
    if "ema12" in wanted:
        overlays["ema12"] = _points(times, ema(close, 12))
    if "ema26" in wanted:
        overlays["ema26"] = _points(times, ema(close, 26))
    if "vwap" in wanted:
        overlays["vwap"] = _points(times, vwap(df))
    if "supertrend" in wanted:
        overlays["supertrend"] = _points(times, supertrend(df))
    if "ichimoku" in wanted:
        cloud = ichimoku(df)
        overlays["ichi_tenkan"] = _points(times, cloud["tenkan"])
        overlays["ichi_kijun"] = _points(times, cloud["kijun"])
        overlays["ichi_span_a"] = _points(times, cloud["span_a"])
        overlays["ichi_span_b"] = _points(times, cloud["span_b"])
    if "donchian" in wanted:
        dc = donchian(df)
        overlays["don_upper"] = _points(times, dc["upper"])
        overlays["don_lower"] = _points(times, dc["lower"])
    if "keltner" in wanted:
        kc = keltner(df)
        overlays["kel_upper"] = _points(times, kc["upper"])
        overlays["kel_mid"] = _points(times, kc["mid"])
        overlays["kel_lower"] = _points(times, kc["lower"])
    if "bb" in wanted:
        mid = close.rolling(20).mean()
        std = close.rolling(20).std()
        overlays["bb_mid"] = _points(times, mid)
        overlays["bb_upper"] = _points(times, mid + 2 * std)
        overlays["bb_lower"] = _points(times, mid - 2 * std)
    if "atr" in wanted:
        oscillators["atr"] = _points(times, atr(df, 14))
    if "rsi" in wanted:
        oscillators["rsi"] = _points(times, rsi(close, 14))
    if "macd" in wanted:
        macd_df = macd(close)
        oscillators["macd"] = _points(times, macd_df["macd"])
        oscillators["macd_signal"] = _points(times, macd_df["signal"])
        oscillators["macd_hist"] = _points(times, macd_df["histogram"])
    if "stoch" in wanted:
        st = stochastic(df)
        oscillators["stoch_k"] = _points(times, st["k"])
        oscillators["stoch_d"] = _points(times, st["d"])
    if "willr" in wanted:
        oscillators["willr"] = _points(times, williams_r(df))
    if "cci" in wanted:
        oscillators["cci"] = _points(times, cci(df))
    if "obv" in wanted:
        oscillators["obv"] = _points(times, obv(df))

    # ---- open-source library -------------------------------------------------
    if "wma" in wanted:
        overlays["wma"] = _points(times, wma(close, 20))
    if "hma" in wanted:
        overlays["hma"] = _points(times, hma(close, 21))
    if "dema" in wanted:
        overlays["dema"] = _points(times, dema(close, 21))
    if "tema" in wanted:
        overlays["tema"] = _points(times, tema(close, 21))
    if "zlema" in wanted:
        overlays["zlema"] = _points(times, zlema(close, 21))
    if "vwma" in wanted:
        overlays["vwma"] = _points(times, vwma(df, 20))
    if "psar" in wanted:
        overlays["psar"] = _points(times, parabolic_sar(df))
    if "pivots" in wanted:
        pv = pivot_points(df)
        for key in ("pivot", "pivot_r1", "pivot_s1", "pivot_r2", "pivot_s2"):
            overlays[key] = _points(times, pv[key])
    if "chandelier" in wanted:
        ce = chandelier_exit(df)
        overlays["chandelier_long"] = _points(times, ce["chandelier_long"])
        overlays["chandelier_short"] = _points(times, ce["chandelier_short"])
    if "adx" in wanted:
        dmi = adx(df)
        oscillators["adx"] = _points(times, dmi["adx"])
        oscillators["plus_di"] = _points(times, dmi["plus_di"])
        oscillators["minus_di"] = _points(times, dmi["minus_di"])
    if "aroon" in wanted:
        ar = aroon(df)
        oscillators["aroon_up"] = _points(times, ar["aroon_up"])
        oscillators["aroon_down"] = _points(times, ar["aroon_down"])
    if "vortex" in wanted:
        vx = vortex(df)
        oscillators["vi_plus"] = _points(times, vx["vi_plus"])
        oscillators["vi_minus"] = _points(times, vx["vi_minus"])
    if "roc" in wanted:
        oscillators["roc"] = _points(times, roc(close, 12))
    if "momentum" in wanted:
        oscillators["momentum"] = _points(times, momentum(close, 10))
    if "trix" in wanted:
        oscillators["trix"] = _points(times, trix(close))
    if "ppo" in wanted:
        pp = ppo(close)
        oscillators["ppo"] = _points(times, pp["ppo"])
        oscillators["ppo_signal"] = _points(times, pp["ppo_signal"])
    if "ao" in wanted:
        oscillators["ao"] = _points(times, awesome_oscillator(df))
    if "uo" in wanted:
        oscillators["uo"] = _points(times, ultimate_oscillator(df))
    if "coppock" in wanted:
        oscillators["coppock"] = _points(times, coppock(close))
    if "kst" in wanted:
        k = kst(close)
        oscillators["kst"] = _points(times, k["kst"])
        oscillators["kst_signal"] = _points(times, k["kst_signal"])
    if "fisher" in wanted:
        oscillators["fisher"] = _points(times, fisher_transform(df))
    if "wavetrend" in wanted:
        wt = wave_trend(df)
        oscillators["wt1"] = _points(times, wt["wt1"])
        oscillators["wt2"] = _points(times, wt["wt2"])
    if "squeeze" in wanted:
        sq = squeeze_momentum(df)
        oscillators["squeeze_momentum"] = _points(times, sq["squeeze_momentum"])
        oscillators["squeeze_on"] = _points(times, sq["squeeze_on"])
    if "bbextras" in wanted:
        extras = bollinger_extras(close)
        oscillators["bb_percent_b"] = _points(times, extras["bb_percent_b"])
        oscillators["bb_bandwidth"] = _points(times, extras["bb_bandwidth"])
    if "elder" in wanted:
        er = elder_ray(df)
        oscillators["bull_power"] = _points(times, er["bull_power"])
        oscillators["bear_power"] = _points(times, er["bear_power"])
    if "mfi" in wanted:
        oscillators["mfi"] = _points(times, mfi(df))
    if "cmf" in wanted:
        oscillators["cmf"] = _points(times, chaikin_money_flow(df))
    if "adline" in wanted:
        oscillators["adline"] = _points(times, accumulation_distribution(df))
    if "chaikin" in wanted:
        oscillators["chaikin"] = _points(times, chaikin_oscillator(df))
    if "fi" in wanted:
        oscillators["fi"] = _points(times, force_index(df))
    if "eom" in wanted:
        oscillators["eom"] = _points(times, ease_of_movement(df))

    volume = [
        {
            "time": int(ts),
            "value": float(vol),
            "color": "#26a69a88" if close_px >= open_px else "#ef535088",
        }
        for ts, vol, close_px, open_px in zip(df["time"], df["volume"], df["close"], df["open"])
    ]
    if vrcs:
        compressed = vrcs["compressed"]
        for i, bar in enumerate(volume):
            if i < len(compressed) and compressed[i]:
                bar["color"] = "#c8a45a66"

    return {"overlays": overlays, "oscillators": oscillators, "volume": volume, "vrcs": vrcs}
