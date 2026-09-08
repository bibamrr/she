from __future__ import annotations

import asyncio
import time

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

from apps.api.app.services.market import fetch_ticker, is_crypto
from apps.api.app.services.overview import quotes as batch_quotes
from apps.api.app.services.yahoo import yahoo_quote

router = APIRouter(tags=["ws"])


def _live_rows(symbols: list[str]) -> list[dict]:
    crypto = [item for item in symbols if is_crypto(item)]
    desk = [item for item in symbols if not is_crypto(item)]
    rows: list[dict] = []
    if desk:
        try:
            rows.extend(yahoo_quote(desk, deep=False))
        except Exception:
            pass
        have = {row.get("symbol") for row in rows}
        missing = [item for item in desk if item not in have]
        if missing:
            try:
                rows.extend(batch_quotes(missing))
            except Exception:
                pass
    if crypto:
        try:
            rows.extend(batch_quotes(crypto))
        except Exception:
            for symbol in crypto:
                try:
                    ticker = fetch_ticker(symbol)
                    rows.append(
                        {
                            "symbol": symbol,
                            "last": ticker.get("last"),
                            "percentage": ticker.get("percentage"),
                        }
                    )
                except Exception:
                    continue
    return rows


@router.websocket("/api/ws/market")
async def market_socket(websocket: WebSocket) -> None:
    await websocket.accept()
    raw = websocket.query_params.get("symbols") or websocket.query_params.get("symbol") or "BTC/USDT"
    symbols = [item.strip() for item in raw.split(",") if item.strip()][:8] or ["BTC/USDT"]
    try:
        while True:
            try:
                found = await asyncio.to_thread(_live_rows, symbols)
                by_symbol = {row.get("symbol"): row for row in found if row}
                quotes = []
                for symbol in symbols:
                    row = by_symbol.get(symbol) or {}
                    quotes.append(
                        {
                            "symbol": symbol,
                            "price": row.get("last"),
                            "percentage": row.get("percentage"),
                            "ts": int(time.time() * 1000),
                        }
                    )
                first = quotes[0]
                if websocket.client_state != WebSocketState.CONNECTED:
                    return
                await websocket.send_json(
                    {
                        "symbol": first["symbol"],
                        "price": first["price"],
                        "percentage": first["percentage"],
                        "ts": first["ts"],
                        "quotes": quotes,
                    }
                )
            except WebSocketDisconnect:
                return
            except Exception as exc:  # noqa: BLE001
                if websocket.client_state != WebSocketState.CONNECTED:
                    return
                try:
                    await websocket.send_json({"error": str(exc), "symbol": symbols[0], "quotes": []})
                except (WebSocketDisconnect, RuntimeError):
                    return
            await asyncio.sleep(1.2)
    except (WebSocketDisconnect, RuntimeError):
        return
