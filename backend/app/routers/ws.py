from __future__ import annotations

import asyncio
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.app.config import get_settings
from backend.app.services.market import fetch_ticker

router = APIRouter(tags=["ws"])


class Hub:
    def __init__(self) -> None:
        self.clients: list[WebSocket] = []

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self.clients.append(ws)

    def disconnect(self, ws: WebSocket) -> None:
        if ws in self.clients:
            self.clients.remove(ws)

    async def broadcast(self, message: dict) -> None:
        dead: list[WebSocket] = []
        payload = json.dumps(message)
        for client in self.clients:
            try:
                await client.send_text(payload)
            except Exception:
                dead.append(client)
        for client in dead:
            self.disconnect(client)


hub = Hub()


@router.websocket("/ws/ticker")
async def ticker_socket(websocket: WebSocket, symbol: str = "BTCUSDT") -> None:
    await hub.connect(websocket)
    settings = get_settings()
    try:
        while True:
            try:
                tick = await asyncio.to_thread(fetch_ticker, symbol)
                await websocket.send_text(json.dumps({"type": "tick", **tick}))
            except Exception as exc:
                await websocket.send_text(json.dumps({"type": "error", "detail": str(exc)}))
            await asyncio.sleep(settings.ticker_broadcast_seconds)
    except WebSocketDisconnect:
        hub.disconnect(websocket)
