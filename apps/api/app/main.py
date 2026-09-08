from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from apps.api.app.config import get_settings
from apps.api.app.db import init_db
from apps.api.app.routers import (
    agents,
    assistant,
    auth,
    hunter,
    indicators,
    market,
    scanner,
    subscriptions,
    system,
    ws,
    integrations,
    admin,
    alerts,
    paper,
    watchlist,
    news,
)

settings = get_settings()
app = FastAPI(title="SHC API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list + ["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(market.router)
app.include_router(scanner.router)
app.include_router(indicators.router)
app.include_router(hunter.router)
app.include_router(agents.router)
app.include_router(subscriptions.router)
app.include_router(assistant.router)
app.include_router(integrations.router)
app.include_router(system.router)
app.include_router(admin.router)
app.include_router(alerts.router)
app.include_router(paper.router)
app.include_router(watchlist.router)
app.include_router(news.router)
app.include_router(ws.router)


@app.on_event("startup")
async def on_startup() -> None:
    # uvicorn only wires up its own loggers, so the background workers stayed
    # silent and there was no way to see whether the desk was ticking.
    for name in ("shc.agents", "shc.alerts"):
        worker_log = logging.getLogger(name)
        worker_log.setLevel(logging.INFO)
        if not worker_log.handlers:
            worker_log.addHandler(logging.StreamHandler())
        worker_log.propagate = False
    init_db()
    app.state.monitor = asyncio.create_task(system.monitor_loop())
    app.state.alerts = asyncio.create_task(alerts.alert_loop())
    app.state.agents = asyncio.create_task(agents.agent_loop())


@app.on_event("shutdown")
async def on_shutdown() -> None:
    for name in ("monitor", "alerts", "agents"):
        task = getattr(app.state, name, None)
        if task:
            task.cancel()


@app.get("/api/health")
def health() -> dict:
    return {"ok": True, "product": "SHC"}


STATIC_DIR = Path(__file__).resolve().parents[2] / "web" / "static"
INDEX_HTML = STATIC_DIR / "index.html"
if INDEX_HTML.exists():
    assets = STATIC_DIR / "assets"
    if assets.exists():
        app.mount("/assets", StaticFiles(directory=assets), name="assets")

    def _index() -> FileResponse:
        return FileResponse(
            INDEX_HTML,
            headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache"},
        )

    @app.get("/")
    def spa_root() -> FileResponse:
        return _index()

    @app.get("/{path:path}")
    def spa_pages(path: str) -> FileResponse:
        if path.startswith("api/") or path.startswith("assets/"):
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Not found")
        return _index()
