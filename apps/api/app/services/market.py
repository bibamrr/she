from __future__ import annotations

import threading
from typing import Any

import ccxt

from apps.api.app.services import stocks

_lock = threading.Lock()
_exchanges: dict[str, ccxt.Exchange] = {}

_CRYPTO_QUOTES = ("USDT", "USDC", "BUSD", "FDUSD", "USD")
_FUTURES_MARKS = {"FUT", "P", "PERP", "USDT"}
_EXCHANGE_ALIASES = {
    "BINANCE": "binance",
    "BINANCEUSDM": "binance",
    "BINANCE-FUTURES": "binance",
}

WATCHLIST = [
    {"symbol": "BTC/USDT", "label": "Bitcoin"},
    {"symbol": "ETH/USDT", "label": "Ethereum"},
    {"symbol": "SOL/USDT", "label": "Solana"},
    {"symbol": "XRP/USDT", "label": "XRP"},
    {"symbol": "BNB/USDT", "label": "BNB"},
]

TIMEFRAMES = [
    {"id": "1s", "label": "1s"},
    {"id": "1m", "label": "1m"},
    {"id": "3m", "label": "3m"},
    {"id": "5m", "label": "5m"},
    {"id": "15m", "label": "15m"},
    {"id": "30m", "label": "30m"},
    {"id": "1h", "label": "1h"},
    {"id": "2h", "label": "2h"},
    {"id": "4h", "label": "4h"},
    {"id": "6h", "label": "6h"},
    {"id": "12h", "label": "12h"},
    {"id": "1d", "label": "1D"},
    {"id": "3d", "label": "3D"},
    {"id": "1w", "label": "1W"},
    {"id": "1M", "label": "1M"},
    {"id": "1Y", "label": "1Y"},
]

TF_SOURCE = {"1Y": "1M"}
TF_MS = {
    "1s": 1_000,
    "1m": 60_000,
    "3m": 180_000,
    "5m": 300_000,
    "15m": 900_000,
    "30m": 1_800_000,
    "1h": 3_600_000,
    "2h": 7_200_000,
    "4h": 14_400_000,
    "6h": 21_600_000,
    "12h": 43_200_000,
    "1d": 86_400_000,
}


def normalize_timeframe(timeframe: str) -> str:
    return TF_SOURCE.get(timeframe, timeframe)


def rows_to_candles(rows: list[list[Any]]) -> list[dict[str, Any]]:
    return [
        {"time": int(ts / 1000), "open": o, "high": h, "low": l, "close": c, "volume": v}
        for ts, o, h, l, c, v in rows
    ]


def sync_ohlcv(rows: list[list[Any]]) -> list[list[Any]]:
    """Deduplicate, sort and drop broken bars so live ticks align with history."""
    by_ts: dict[int, list[Any]] = {}
    for row in rows:
        if not row or len(row) < 6:
            continue
        ts = int(row[0])
        if ts <= 0:
            continue
        try:
            o, h, l, c, v = (float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5] or 0))
        except (TypeError, ValueError):
            continue
        if h < l or o <= 0 or c <= 0:
            continue
        high = max(h, o, c)
        low = min(l, o, c)
        by_ts[ts] = [ts, o, high, low, c, max(v, 0.0)]
    return [by_ts[ts] for ts in sorted(by_ts)]


def fill_crypto_gaps(rows: list[list[Any]], timeframe: str, max_fill: int = 3) -> list[list[Any]]:
    """Insert flat bars for 1–3 missing crypto intervals so live ticks stay aligned."""
    step = TF_MS.get(timeframe)
    if not step or len(rows) < 3:
        return rows
    out = [rows[0]]
    for row in rows[1:]:
        prev = out[-1]
        missing = int(round((row[0] - prev[0]) / step)) - 1
        if 1 <= missing <= max_fill:
            close = prev[4]
            for index in range(1, missing + 1):
                out.append([prev[0] + step * index, close, close, close, close, 0.0])
        out.append(row)
    return out


def delay_ohlcv(rows: list[list[Any]], drop_last: int = 3) -> list[list[Any]]:
    """Explorer equity feed: hide the most recent unfinished bars."""
    if len(rows) <= drop_last + 20:
        return rows[:-1] if len(rows) > 1 else rows
    return rows[:-drop_last]


def parse_market_symbol(symbol: str) -> dict[str, Any]:
    """Split a desk symbol into display pair, exchange, and spot/futures."""
    raw = (symbol or "").strip().upper().replace(" ", "")
    exchange = "binance"
    market_type = "spot"
    empty = {
        "desk": "",
        "ccxt": "",
        "display": "",
        "exchange": "",
        "market_type": "",
        "crypto": False,
    }
    if not raw:
        return empty
    if ":" in raw:
        left, right = raw.split(":", 1)
        if left in _EXCHANGE_ALIASES:
            exchange = _EXCHANGE_ALIASES[left]
            raw = right
            if left == "BINANCEUSDM":
                market_type = "futures"
    if ":" in raw:
        body, mark = raw.rsplit(":", 1)
        if mark in _FUTURES_MARKS:
            raw = body
            market_type = "futures"
    if "/" not in raw:
        for quote in _CRYPTO_QUOTES:
            if raw.endswith(quote) and len(raw) > len(quote):
                raw = f"{raw[: -len(quote)]}/{quote}"
                break
    display = raw
    if "/" not in display:
        original = (symbol or "").strip().upper()
        return {**empty, "desk": original, "display": original}
    desk = f"{display}:FUT" if market_type == "futures" else display
    ccxt_symbol = f"{display}:USDT" if market_type == "futures" else display
    return {
        "desk": desk,
        "ccxt": ccxt_symbol,
        "display": display,
        "exchange": exchange,
        "market_type": market_type,
        "crypto": True,
    }


def desk_symbol(symbol: str) -> str:
    spec = parse_market_symbol(symbol)
    return spec["desk"] or (symbol or "").strip().upper()


def get_exchange(market_type: str = "spot") -> ccxt.Exchange:
    kind = "futures" if str(market_type or "").lower() == "futures" else "spot"
    with _lock:
        if kind not in _exchanges:
            factory = ccxt.binanceusdm if kind == "futures" else ccxt.binance
            _exchanges[kind] = factory({"enableRateLimit": True})
        return _exchanges[kind]


def is_crypto(symbol: str) -> bool:
    return bool(parse_market_symbol(symbol)["crypto"]) or "/" in (symbol or "")


def fetch_ohlcv(symbol: str, timeframe: str, limit: int = 300, delayed: bool = False) -> list[list[Any]]:
    tf = normalize_timeframe(timeframe)
    extra = 8 if delayed else 0
    spec = parse_market_symbol(symbol)
    if not spec["crypto"]:
        rows = stocks.stock_ohlcv(symbol, tf, limit + extra)
        synced = sync_ohlcv(rows)
        return delay_ohlcv(synced) if delayed else synced
    exchange = get_exchange(spec["market_type"])
    try:
        rows = exchange.fetch_ohlcv(spec["ccxt"], timeframe=tf, limit=limit + extra)
    except Exception:
        if tf == "1s":
            rows = exchange.fetch_ohlcv(spec["ccxt"], timeframe="1m", limit=limit + extra)
        else:
            raise
    synced = fill_crypto_gaps(sync_ohlcv(rows), tf)
    return delay_ohlcv(synced, 1) if delayed and not spec["crypto"] else synced[-limit:]


def fetch_ticker(symbol: str) -> dict[str, Any]:
    spec = parse_market_symbol(symbol)
    if not spec["crypto"]:
        row = stocks.quote(symbol)
        if not row:
            raise RuntimeError(f"No quote for {symbol}")
        return {
            "last": row.get("last"),
            "percentage": row.get("percentage"),
            "bid": row.get("last"),
            "ask": row.get("last"),
            "high": None,
            "low": None,
            "baseVolume": row.get("volume"),
            "venue": row.get("venue"),
            "name": row.get("name"),
        }
    data = get_exchange(spec["market_type"]).fetch_ticker(spec["ccxt"])
    data["exchange"] = spec["exchange"]
    data["market_type"] = spec["market_type"]
    data["display_symbol"] = spec["display"]
    data["symbol"] = spec["desk"]
    return data


def fetch_order_book(symbol: str, limit: int = 50) -> dict[str, Any]:
    spec = parse_market_symbol(symbol)
    if not spec["crypto"]:
        return get_exchange().fetch_order_book(symbol, limit=limit)
    return get_exchange(spec["market_type"]).fetch_order_book(spec["ccxt"], limit=limit)
