from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import ccxt
from fastapi import HTTPException

_exchange: ccxt.binance | None = None


def get_exchange() -> ccxt.binance:
    global _exchange
    if _exchange is None:
        _exchange = ccxt.binance({"enableRateLimit": True})
    return _exchange


def to_ccxt_symbol(symbol: str) -> str:
    raw = symbol.upper().replace("-", "").replace("_", "")
    if "/" in symbol:
        return symbol.upper()
    if raw.endswith("USDT"):
        return f"{raw[:-4]}/USDT"
    if raw.endswith("USD"):
        return f"{raw[:-3]}/USD"
    return f"{raw}/USDT"


def to_binance_symbol(symbol: str) -> str:
    return to_ccxt_symbol(symbol).replace("/", "")


def fetch_ticker(symbol: str) -> dict[str, Any]:
    exchange = get_exchange()
    pair = to_ccxt_symbol(symbol)
    try:
        ticker = exchange.fetch_ticker(pair)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"Market data unavailable: {exc}") from exc
    return {
        "symbol": pair,
        "binance_symbol": to_binance_symbol(symbol),
        "last": float(ticker["last"] or 0),
        "bid": float(ticker.get("bid") or 0),
        "ask": float(ticker.get("ask") or 0),
        "high": float(ticker.get("high") or 0),
        "low": float(ticker.get("low") or 0),
        "percentage": float(ticker.get("percentage") or 0),
        "quote_volume": float(ticker.get("quoteVolume") or 0),
        "timestamp_ms": int(ticker.get("timestamp") or datetime.now(timezone.utc).timestamp() * 1000),
    }


def fetch_ohlcv(symbol: str, timeframe: str = "1h", limit: int = 300) -> list[dict[str, Any]]:
    exchange = get_exchange()
    pair = to_ccxt_symbol(symbol)
    try:
        rows = exchange.fetch_ohlcv(pair, timeframe=timeframe, limit=limit)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"OHLCV unavailable: {exc}") from exc
    return [
        {
            "time": int(ts / 1000),
            "timestamp_ms": int(ts),
            "open": float(o),
            "high": float(h),
            "low": float(l),
            "close": float(c),
            "volume": float(v),
        }
        for ts, o, h, l, c, v in rows
    ]


def fetch_order_book(symbol: str, limit: int = 20) -> dict[str, Any]:
    exchange = get_exchange()
    pair = to_ccxt_symbol(symbol)
    try:
        book = exchange.fetch_order_book(pair, limit=limit)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"Order book unavailable: {exc}") from exc
    return {
        "symbol": pair,
        "bids": [{"price": float(p), "amount": float(a)} for p, a in book["bids"][:limit]],
        "asks": [{"price": float(p), "amount": float(a)} for p, a in book["asks"][:limit]],
        "timestamp_ms": int(book.get("timestamp") or datetime.now(timezone.utc).timestamp() * 1000),
    }


WATCHLIST = [
    "BTC/USDT",
    "ETH/USDT",
    "SOL/USDT",
    "XRP/USDT",
    "BNB/USDT",
    "DOGE/USDT",
]
