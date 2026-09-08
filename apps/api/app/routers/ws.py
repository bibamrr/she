from __future__ import annotations

import asyncio
import time
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

from apps.api.app.services.binance_stream import iter_ticks
from apps.api.app.services.market import is_crypto, parse_market_symbol
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
            from apps.api.app.services.market import fetch_ticker

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


def _split_symbols(symbols: list[str]) -> tuple[list[str], list[str], list[str]]:
    spot: list[str] = []
    futures: list[str] = []
    desk: list[str] = []
    for symbol in symbols:
        spec = parse_market_symbol(symbol)
        if spec["crypto"] and spec["market_type"] == "futures":
            futures.append(spec["desk"] or symbol)
        elif spec["crypto"]:
            spot.append(spec["desk"] or symbol)
        else:
            desk.append(symbol)
    return spot, futures, desk


@router.websocket("/api/ws/market")
async def market_socket(websocket: WebSocket) -> None:
    await websocket.accept()
    raw = websocket.query_params.get("symbols") or websocket.query_params.get("symbol") or "BTC/USDT"
    symbols = [item.strip() for item in raw.split(",") if item.strip()][:8] or ["BTC/USDT"]
    spot, futures, desk = _split_symbols(symbols)
    alias = {parse_market_symbol(item)["desk"] or item: item for item in symbols}
    latest: dict[str, dict[str, Any]] = {item: {"symbol": item, "price": None, "percentage": None} for item in symbols}
    lock = asyncio.Lock()

    async def emit(symbol: str, price: Any, percentage: Any, ts: int) -> None:
        key = alias.get(symbol) or symbol
        async with lock:
            row = latest.get(key) or {"symbol": key}
            row["symbol"] = key
            row["price"] = price
            if percentage is not None:
                row["percentage"] = percentage
            row["ts"] = ts
            latest[key] = row
            quotes = [latest.get(item) or {"symbol": item, "price": None, "percentage": None, "ts": ts} for item in symbols]
            first = quotes[0]
        if websocket.client_state != WebSocketState.CONNECTED:
            return
        await websocket.send_json(
            {
                "symbol": first.get("symbol"),
                "price": first.get("price"),
                "percentage": first.get("percentage"),
                "ts": ts,
                "quotes": quotes,
                "live": True,
            }
        )

    async def stream_crypto(group: list[str], use_futures: bool) -> None:
        if not group:
            return
        async for tick in iter_ticks(group, futures=use_futures):
            if websocket.client_state != WebSocketState.CONNECTED:
                return
            try:
                await emit(tick["symbol"], tick["price"], tick.get("percentage"), tick.get("ts") or int(time.time() * 1000))
            except (WebSocketDisconnect, RuntimeError):
                return

    async def poll_rest() -> None:
        needed = list(desk)
        while websocket.client_state == WebSocketState.CONNECTED:
            try:
                found = await asyncio.to_thread(_live_rows, needed or symbols if not (spot or futures) else needed)
                now = int(time.time() * 1000)
                for row in found:
                    symbol = row.get("symbol")
                    if not symbol:
                        continue
                    await emit(symbol, row.get("last"), row.get("percentage"), now)
            except WebSocketDisconnect:
                return
            except Exception as exc:  # noqa: BLE001
                if websocket.client_state != WebSocketState.CONNECTED:
                    return
                try:
                    await websocket.send_json({"error": str(exc), "symbol": symbols[0], "quotes": []})
                except (WebSocketDisconnect, RuntimeError):
                    return
            await asyncio.sleep(2.0 if needed else 30.0)

    tasks = []
    if spot:
        tasks.append(asyncio.create_task(stream_crypto(spot, False)))
    if futures:
        tasks.append(asyncio.create_task(stream_crypto(futures, True)))
    if desk or not (spot or futures):
        tasks.append(asyncio.create_task(poll_rest()))
    if not tasks:
        return
    try:
        await asyncio.gather(*tasks)
    except (WebSocketDisconnect, RuntimeError):
        return
    finally:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
