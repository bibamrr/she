"""Public Binance market-data WebSocket (spot vision host + USDM futures)."""

from __future__ import annotations

import asyncio
import json
from typing import Any, AsyncIterator, Optional

import websockets

from apps.api.app.services.market import parse_market_symbol

SPOT_WS = "wss://data-stream.binance.vision/stream"
FUTURES_WS = "wss://fstream.binance.com/stream"


def stream_id(symbol: str) -> str:
    spec = parse_market_symbol(symbol)
    return (spec["display"] or symbol).replace("/", "").replace(":", "").lower()


def desk_symbol(symbol: str) -> str:
    spec = parse_market_symbol(symbol)
    return spec["desk"] or symbol


def stream_url(symbols: list[str], *, futures: bool = False) -> str:
    parts: list[str] = []
    for symbol in symbols:
        sid = stream_id(symbol)
        parts.append(f"{sid}@aggTrade")
        parts.append(f"{sid}@miniTicker")
    host = FUTURES_WS if futures else SPOT_WS
    return f"{host}?streams={'/'.join(dict.fromkeys(parts))}"


def parse_tick(message: dict[str, Any], symbol_by_id: dict[str, str]) -> Optional[dict[str, Any]]:
    payload = message.get("data") or message
    raw = str(payload.get("s") or "").lower()
    desk = symbol_by_id.get(raw)
    if not desk:
        stream = str(message.get("stream") or "")
        desk = symbol_by_id.get(stream.split("@")[0].lower())
    if not desk:
        return None
    price = payload.get("p") or payload.get("c")
    try:
        last = float(price)
    except (TypeError, ValueError):
        return None
    pct = None
    open_px = payload.get("o")
    if open_px is not None:
        try:
            opened = float(open_px)
            if opened:
                pct = ((last - opened) / opened) * 100
        except (TypeError, ValueError):
            pct = None
    event_ts = payload.get("E") or payload.get("T") or payload.get("t")
    try:
        ts = int(event_ts)
    except (TypeError, ValueError):
        ts = 0
    return {
        "symbol": desk,
        "price": last,
        "percentage": pct,
        "ts": ts,
        "event": str(payload.get("e") or ""),
    }


async def iter_ticks(symbols: list[str], *, futures: bool = False) -> AsyncIterator[dict[str, Any]]:
    wanted = [item for item in symbols if item]
    if not wanted:
        return
    mapping = {stream_id(item): desk_symbol(item) for item in wanted}
    url = stream_url(wanted, futures=futures)
    delay = 1.0
    while True:
        try:
            async with websockets.connect(url, ping_interval=20, ping_timeout=20, close_timeout=5) as ws:
                delay = 1.0
                async for raw in ws:
                    try:
                        msg = json.loads(raw)
                    except json.JSONDecodeError:
                        continue
                    if not isinstance(msg, dict):
                        continue
                    tick = parse_tick(msg, mapping)
                    if tick:
                        yield tick
        except asyncio.CancelledError:
            raise
        except Exception:
            await asyncio.sleep(delay)
            delay = min(delay * 2.0, 12.0)
