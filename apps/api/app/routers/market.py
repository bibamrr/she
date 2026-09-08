from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from apps.api.app.services.market import TIMEFRAMES, WATCHLIST, fetch_ohlcv, normalize_timeframe, rows_to_candles, fetch_ticker

router = APIRouter(prefix="/api/market", tags=["market"])


@router.get("/symbols")
def symbols() -> dict:
    return {"symbols": WATCHLIST, "timeframes": TIMEFRAMES}


@router.get("/ticker")
def ticker(symbol: str = Query(default="BTC/USDT")) -> dict:
    try:
        data = fetch_ticker(symbol)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return {
        "symbol": data.get("symbol") or symbol,
        "display_symbol": data.get("display_symbol") or symbol,
        "exchange": data.get("exchange") or "",
        "market_type": data.get("market_type") or "",
        "last": data.get("last"),
        "bid": data.get("bid"),
        "ask": data.get("ask"),
        "percentage": data.get("percentage"),
        "high": data.get("high"),
        "low": data.get("low"),
        "baseVolume": data.get("baseVolume"),
    }


@router.get("/ohlcv")
def ohlcv(
    symbol: str = Query(default="BTC/USDT"),
    timeframe: str = Query(default="15m"),
    limit: int = Query(default=400, ge=20, le=1500),
) -> dict:
    source = normalize_timeframe(timeframe)
    try:
        rows = fetch_ohlcv(symbol, source, limit)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "source_timeframe": source,
        "candles": rows_to_candles(rows),
    }
