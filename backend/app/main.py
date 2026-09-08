from __future__ import annotations

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import get_settings
from backend.app.db import init_db
from backend.app.routers import agents, auth, billing, market
from backend.app.routers.ws import router as ws_router
from backend.app.seed import seed_plans
from backend.app.db import engine
from sqlmodel import Session

settings = get_settings()
app = FastAPI(title=settings.project_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = APIRouter(prefix=settings.api_prefix)
api.include_router(auth.router)
api.include_router(billing.router)
api.include_router(market.router)
api.include_router(agents.router)
app.include_router(api)
app.include_router(ws_router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    with Session(engine) as session:
        seed_plans(session)


@app.get("/health")
def health() -> dict:
    return {"ok": True, "name": settings.project_name}
