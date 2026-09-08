from __future__ import annotations

from backend.app.services.market import WATCHLIST, fetch_ticker


async def ticker_payload(symbol: str) -> dict:
    return fetch_ticker(symbol)


async def watchlist_tickers() -> list[dict]:
    rows = []
    for symbol in WATCHLIST:
        try:
            rows.append(fetch_ticker(symbol))
        except Exception:
            continue
    return rows
