from __future__ import annotations

from fastapi import APIRouter, Query

from backend.app.services.market import WATCHLIST, fetch_ohlcv, fetch_order_book, fetch_ticker

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/watchlist")
def watchlist() -> dict:
    return {"symbols": WATCHLIST}


@router.get("/ticker")
def ticker(symbol: str = Query("BTCUSDT")) -> dict:
    return fetch_ticker(symbol)


@router.get("/ohlcv")
def ohlcv(
    symbol: str = Query("BTCUSDT"),
    timeframe: str = Query("1h"),
    limit: int = Query(300, ge=50, le=1500),
) -> dict:
    candles = fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    return {"symbol": symbol, "timeframe": timeframe, "candles": candles}


@router.get("/orderbook")
def orderbook(symbol: str = Query("BTCUSDT"), limit: int = Query(20, ge=5, le=100)) -> dict:
    return fetch_order_book(symbol, limit=limit)
