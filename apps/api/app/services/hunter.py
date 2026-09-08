from __future__ import annotations

import gc
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Any

import pandas as pd

from apps.api.app.services.market import fetch_ohlcv
from apps.api.app.services.scanner import crypto_universe
from apps.api.app.services.stables import has_tradable_volatility, skip_crypto_hunter
from apps.api.app.services.yahoo import _cached
from engine.backtest import evaluate_signals
from engine.mtf import confluence
from engine.shc_orchestrator import ohlcv_to_df
from engine.vrcs import compute_vrcs
from indicators.volatility import atr

DEFAULT_MTF = ["15m", "1h", "4h"]
DESKS = ("crypto", "tadawul", "us", "europe", "asia", "commodities")
EQUITY_SCAN_CAP = 16

# One shared pool plus a gate on the fan-out scans: without it, a handful of
# concurrent requests would hold hundreds of dataframes in memory at once.
_POOL = ThreadPoolExecutor(max_workers=10, thread_name_prefix="shc-scan")
_HEAVY_GATE = threading.Semaphore(2)


def _fan_out(fn, items: list[Any]) -> list[Any]:
    with _HEAVY_GATE:
        try:
            return list(_POOL.map(fn, items))
        finally:
            gc.collect()


def load_frame(symbol: str, timeframe: str, limit: int = 300) -> pd.DataFrame:
    rows = fetch_ohlcv(symbol, timeframe, limit)
    df = ohlcv_to_df(rows)
    df["time"] = [int(r[0] / 1000) for r in rows]
    return df


def liquid_universe(top: int = 40) -> list[dict[str, Any]]:
    rows = [
        row
        for row in crypto_universe()
        if (row.get("quote_volume") or 0) > 0 and not skip_crypto_hunter(row.get("symbol") or "", row)
    ]
    rows.sort(key=lambda r: r.get("quote_volume") or 0, reverse=True)
    return rows[:top]


def _normalize_venue(venue: str) -> str:
    key = (venue or "crypto").strip().lower()
    return key if key in DESKS else "crypto"


def desk_universe(venue: str, top: int = 40) -> list[dict[str, Any]]:
    desk = _normalize_venue(venue)
    if desk == "crypto":
        return liquid_universe(top)
    from apps.api.app.services import stocks

    cap = min(max(int(top), 8), EQUITY_SCAN_CAP)
    rows = stocks.universe(desk, limit=max(cap * 3, 40))
    rows.sort(
        key=lambda row: float(row.get("volume") or row.get("quote_volume") or row.get("market_cap") or 0),
        reverse=True,
    )
    return rows[:cap]


def _px(value: float) -> float:
    magnitude = abs(value)
    if magnitude >= 1000:
        return round(value, 2)
    if magnitude >= 1:
        return round(value, 4)
    return round(value, 6)


def _infer_side(state: str, recent: dict[str, Any] | None, df: pd.DataFrame) -> str:
    if recent and recent.get("side") in ("bullish", "bearish"):
        return str(recent["side"])
    label = state or ""
    if "bearish" in label:
        return "bearish"
    if "bullish" in label:
        return "bullish"
    if len(df) >= 8:
        return "bullish" if float(df["close"].iloc[-1]) >= float(df["close"].iloc[-8]) else "bearish"
    return "bullish"


def _setup_levels(df: pd.DataFrame, side: str) -> dict[str, float]:
    entry = float(df["close"].iloc[-1])
    try:
        last_atr = float(atr(df, 14).iloc[-1] or 0)
    except Exception:
        last_atr = 0.0
    distance = last_atr * 1.5 if last_atr > 0 else abs(entry) * 0.01
    if side == "bearish":
        stop = entry + distance
        target = entry - distance * 2
    else:
        stop = entry - distance
        target = entry + distance * 2
    return {"entry": _px(entry), "stop": _px(stop), "target": _px(target)}


def _scan_one(
    symbol: str,
    timeframe: str,
    min_confidence: float,
    volume_spike: float,
    venue: str = "crypto",
) -> dict[str, Any] | None:
    try:
        bars = 140 if venue != "crypto" else 220
        df = load_frame(symbol, timeframe, bars)
    except Exception:
        return None
    if len(df) < 60:
        return None
    if venue == "crypto":
        if skip_crypto_hunter(symbol):
            return None
        if not has_tradable_volatility(df):
            return None
    vrcs = compute_vrcs(df)
    dash = vrcs["dashboard"]
    signals = vrcs["signals"]
    last_signal = signals[-1] if signals else None
    recent = None
    if last_signal is not None:
        bar_index = df.index[df["time"] == last_signal["time"]]
        if len(bar_index):
            age = len(df) - 1 - int(bar_index[0])
            if age <= 3:
                recent = {**last_signal, "bars_ago": age}

    avg_vol = float(df["volume"].tail(20).mean() or 0)
    last_vol = float(df["volume"].iloc[-1])
    vol_ratio = (last_vol / avg_vol) if avg_vol > 0 else 0.0
    quiet_surge = False
    if len(df) >= 3:
        rng = float(df["high"].iloc[-1] - df["low"].iloc[-1])
        avg_rng = float((df["high"] - df["low"]).tail(20).mean() or 0)
        quiet_surge = bool(avg_rng > 0 and rng <= avg_rng * 0.75 and vol_ratio >= volume_spike)

    state = dash["regime"]
    confidence = float(dash["confidence"] or 0)
    if recent:
        confidence = max(confidence, float(recent["confidence"]))
        state = f"spring_{recent['side']}"

    passes = confidence >= min_confidence or quiet_surge
    if not passes:
        return None

    side = _infer_side(state, recent, df)
    levels = _setup_levels(df, side)
    return {
        "symbol": symbol,
        "venue": venue,
        "timeframe": timeframe,
        "state": state,
        "side": side,
        "confidence": round(confidence, 1),
        "streak": dash["streak"],
        "volume_ratio": round(vol_ratio, 2),
        "quiet_volume_surge": quiet_surge,
        "last_price": levels["entry"],
        "entry": levels["entry"],
        "stop": levels["stop"],
        "target": levels["target"],
        "signal": recent,
        "parts": dash.get("parts"),
        "source": "hunter",
    }


def hunt(
    timeframe: str = "15m",
    top: int = 40,
    min_confidence: float = 75.0,
    volume_spike: float = 2.0,
    venue: str = "crypto",
) -> dict[str, Any]:
    desk = _normalize_venue(venue)
    cap = min(int(top), EQUITY_SCAN_CAP) if desk != "crypto" else int(top)
    key = f"hunt:nv2:{desk}:{timeframe}:{cap}:{min_confidence}:{volume_spike}"

    def load() -> dict[str, Any]:
        universe = desk_universe(desk, cap)
        symbols = [row["symbol"] for row in universe]
        found = _fan_out(lambda s: _scan_one(s, timeframe, min_confidence, volume_spike, desk), symbols)
        hits = [h for h in found if h]
        hits.sort(key=lambda h: (h["confidence"], h["volume_ratio"]), reverse=True)
        return {
            "venue": desk,
            "timeframe": timeframe,
            "scanned": len(symbols),
            "hits": hits,
            "elite": [h for h in hits if h["confidence"] >= 90],
            "quiet_surges": [h for h in hits if h["quiet_volume_surge"]],
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    return _cached(key, 45, load)


def is_followable(hit: dict[str, Any], min_confidence: float = 60.0) -> bool:
    """Any live Hunter setup the execution bot may follow (not an invented fill)."""
    if not hit or (hit.get("source") not in {None, "", "hunter"}):
        return False
    symbol = str(hit.get("symbol") or "")
    venue = _normalize_venue(str(hit.get("venue") or "crypto"))
    if venue == "crypto" and skip_crypto_hunter(symbol):
        return False
    if float(hit.get("confidence") or 0) < float(min_confidence):
        return False
    entry = float(hit.get("entry") or hit.get("last_price") or 0)
    stop = float(hit.get("stop") or 0)
    target = float(hit.get("target") or 0)
    return entry > 0 and stop > 0 and target > 0


def is_launchable(hit: dict[str, Any], min_confidence: float) -> bool:
    """Confirmed Hunter opportunity: spring or elite, never a client-invented fill."""
    if not hit or (hit.get("source") not in {None, "", "hunter"}):
        return False
    symbol = str(hit.get("symbol") or "")
    venue = _normalize_venue(str(hit.get("venue") or "crypto"))
    if venue == "crypto" and skip_crypto_hunter(symbol):
        return False
    confidence = float(hit.get("confidence") or 0)
    if confidence < float(min_confidence):
        return False
    state = str(hit.get("state") or "")
    signal = hit.get("signal") or {}
    spring = state.startswith("spring") or signal.get("side") in {"bullish", "bearish"}
    elite = confidence >= 90
    if not (spring or elite):
        return False
    entry = float(hit.get("entry") or hit.get("last_price") or 0)
    stop = float(hit.get("stop") or 0)
    target = float(hit.get("target") or 0)
    return entry > 0 and stop > 0 and target > 0


def match_official(hit: dict[str, Any], min_confidence: float) -> dict[str, Any] | None:
    """Resolve a request against the live Hunter book. Execution may not invent levels."""
    symbol = str(hit.get("symbol") or "").strip().upper()
    if not symbol:
        return None
    venue = _normalize_venue(str(hit.get("venue") or "crypto"))
    timeframe = str(hit.get("timeframe") or "15m")
    if venue == "crypto" and skip_crypto_hunter(symbol):
        return None
    scan_floor = min(75.0, float(min_confidence))
    data = hunt(timeframe, 24 if venue == "crypto" else 16, scan_floor, 1.5, venue=venue)
    for official in data.get("hits") or []:
        if str(official.get("symbol") or "").upper() != symbol:
            continue
        if is_followable(official, min(60.0, float(min_confidence))):
            return official
    return None


def multi_timeframe(symbol: str, timeframes: list[str] | None = None) -> dict[str, Any]:
    tfs = timeframes or DEFAULT_MTF
    frames: dict[str, pd.DataFrame] = {}
    for tf in tfs:
        try:
            frames[tf] = load_frame(symbol, tf, 220)
        except Exception:
            continue
    result = confluence(frames)
    result["symbol"] = symbol
    return result


def backtest(symbol: str, timeframe: str, horizon: int = 24, reward_multiple: float = 2.0) -> dict[str, Any]:
    df = load_frame(symbol, timeframe, 1000)
    result = evaluate_signals(df, horizon=horizon, reward_multiple=reward_multiple)
    result["symbol"] = symbol
    result["timeframe"] = timeframe
    return result


def correlation_matrix(timeframe: str = "1h", top: int = 12, limit: int = 200) -> dict[str, Any]:
    key = f"corr:{timeframe}:{top}:{limit}"

    def load() -> dict[str, Any]:
        universe = liquid_universe(top)
        symbols = ["BTC/USDT"] + [r["symbol"] for r in universe if r["symbol"] != "BTC/USDT"]
        symbols = symbols[:top]

        def series(symbol: str):
            try:
                df = load_frame(symbol, timeframe, limit)
                return symbol, df["close"].pct_change().dropna().reset_index(drop=True)
            except Exception:
                return symbol, None

        pairs = _fan_out(series, symbols)

        valid = {s: v for s, v in pairs if v is not None and len(v) > 30}
        if not valid:
            return {"symbols": [], "matrix": [], "btc_correlation": []}
        length = min(len(v) for v in valid.values())
        frame = pd.DataFrame({s: v.tail(length).reset_index(drop=True) for s, v in valid.items()})
        corr = frame.corr().round(3)
        names = list(corr.columns)
        matrix = [[float(corr.iloc[i, j]) for j in range(len(names))] for i in range(len(names))]
        btc = []
        if "BTC/USDT" in corr.columns:
            btc = [
                {"symbol": s, "correlation": float(corr.loc[s, "BTC/USDT"])}
                for s in names
                if s != "BTC/USDT"
            ]
            btc.sort(key=lambda r: r["correlation"], reverse=True)
        return {"symbols": names, "matrix": matrix, "btc_correlation": btc, "timeframe": timeframe}

    return _cached(key, 120, load)


def session_heatmap(symbol: str = "BTC/USDT", timeframe: str = "1h", limit: int = 1000) -> dict[str, Any]:
    key = f"heat:{symbol}:{timeframe}:{limit}"

    def load() -> dict[str, Any]:
        df = load_frame(symbol, timeframe, limit)
        vrcs = compute_vrcs(df)
        compressed = vrcs["compressed"]
        springs = {int(s["time"]): s for s in vrcs["signals"]}
        hours = {h: {"hour": h, "compression": 0, "springs": 0, "avg_confidence": 0.0} for h in range(24)}
        conf_acc: dict[int, list[float]] = {h: [] for h in range(24)}
        for i, ts in enumerate(df["time"].tolist()):
            hour = datetime.fromtimestamp(int(ts), tz=timezone.utc).hour
            if i < len(compressed) and compressed[i]:
                hours[hour]["compression"] += 1
            signal = springs.get(int(ts))
            if signal:
                hours[hour]["springs"] += 1
                conf_acc[hour].append(signal["confidence"])
        for hour, values in conf_acc.items():
            if values:
                hours[hour]["avg_confidence"] = round(sum(values) / len(values), 1)
        rows = list(hours.values())
        best = sorted(rows, key=lambda r: (r["springs"], r["compression"]), reverse=True)[:4]
        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "hours": rows,
            "peak_hours": [r["hour"] for r in best],
            "timezone": "UTC",
        }

    return _cached(key, 300, load)
