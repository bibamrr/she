from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from apps.api.app.db import get_session
from apps.api.app.models import User
from apps.api.app.schemas import AnalyzeRequest
from apps.api.app.security import get_current_user
from apps.api.app.services import access, auditor, execution, insight, swarm
from apps.api.app.services.market import fetch_ohlcv, fetch_order_book
from engine.agent_copy import localize_analysis
from engine.coordinator import BUY, SELL
from engine.shc_orchestrator import run_shc_analysis

logger = logging.getLogger("shc.agents")

router = APIRouter(prefix="/api/agents", tags=["agents"])


class DeskPayload(BaseModel):
    enabled: Optional[bool] = None
    venue: Optional[str] = None
    max_open: Optional[int] = None
    risk_pct: Optional[float] = None


class TickPayload(BaseModel):
    venue: Optional[str] = None


class HitPayload(BaseModel):
    symbol: str
    side: str = "bullish"
    entry: Optional[float] = None
    stop: Optional[float] = None
    target: Optional[float] = None
    confidence: float = 0
    timeframe: str = "15m"
    venue: str = "crypto"
    state: str = ""
    last_price: Optional[float] = None
    signal: Optional[dict[str, Any]] = None


class AuditPayload(BaseModel):
    apply: bool = True


@router.post("/analyze")
async def analyze(payload: AnalyzeRequest, user: User = Depends(access.require_feature("agents"))) -> dict:
    if user.plan == "free":
        payload.lookback = min(payload.lookback, 180)
    try:
        ohlcv = await asyncio.to_thread(fetch_ohlcv, payload.symbol, payload.timeframe, payload.lookback)
        book = await asyncio.to_thread(fetch_order_book, payload.symbol, 50)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    extras = {
        "news": await asyncio.to_thread(swarm._headlines, payload.symbol, ""),
        "hunter": {"symbol": payload.symbol, "entry": None},
    }
    result = run_shc_analysis(payload.symbol, payload.timeframe, ohlcv, book, extras=extras)
    localize_analysis(result, payload.locale or user.locale or "ar")
    try:
        result["profile"] = await asyncio.to_thread(insight.fundamentals, payload.symbol, payload.timeframe)
    except Exception:
        result["profile"] = None
    decided = swarm._decide(list(result.get("agents") or []))
    vote = str(decided.get("vote") or "")
    setup = {
        "vote": vote,
        "side": decided.get("direction"),
        "entry": 0.0,
        "stop": 0.0,
        "target": 0.0,
    }
    if vote in {BUY, SELL}:
        pack = swarm.analysis_package(result, vote, {"entry": result.get("last_price")})
        setup.update(pack)
    result["coordinator"] = decided.get("verdict") or {}
    result["status"] = decided.get("status")
    result["vote"] = vote
    result["setup"] = setup
    result["requested_by"] = user.email
    result["plan"] = user.plan
    return result


@router.get("/desk")
def agent_desk(user: User = Depends(get_current_user), session: Session = Depends(get_session)) -> dict[str, Any]:
    return execution.status(session, user)


@router.post("/desk")
def update_desk(
    payload: DeskPayload,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    desk = execution.save_desk(
        session,
        user,
        enabled=payload.enabled,
        venue=payload.venue,
        max_open=payload.max_open,
        risk_pct=payload.risk_pct,
    )
    return {"ok": True, "desk": execution.serialize_desk(desk)}


@router.post("/execution/tick")
def execution_tick(
    payload: TickPayload = TickPayload(),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    try:
        return execution.tick(session, user, payload.venue)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/execution/from-hit")
def execution_from_hit(
    payload: HitPayload,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    try:
        return execution.execute_hit(session, user, payload.model_dump())
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/auditor/review")
def auditor_review(
    payload: AuditPayload = AuditPayload(),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    try:
        return auditor.review(session, user, apply_corrections=payload.apply)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/swarm")
def swarm_board(
    user: User = Depends(access.require_feature("agents")),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    data = swarm.board(session)
    data["errors"] = auditor.classify_agents(session, user)
    return data


@router.get("/reports")
def agent_reports(
    kind: str = "",
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    return {"reports": execution.list_reports(session, user, kind, 24)}


AGENT_CYCLE_SECONDS = 60
AGENT_MIN_IDLE_SECONDS = 20


async def agent_loop() -> None:
    await asyncio.sleep(15)
    cycle = 0
    while True:
        started = time.perf_counter()
        try:
            from apps.api.app.services import botday

            rolled = await asyncio.to_thread(botday.maybe_roll)
            if rolled:
                logger.info(
                    "bot day reset day=%s opened=%s wallet=%s",
                    rolled.get("day"),
                    rolled.get("opened"),
                    rolled.get("wallet"),
                )
            report = await asyncio.to_thread(execution.tick_all)
            logger.info(
                "execution tick venue=%s tfs=%s hits=%s approved=%s opened=%s took=%.1fs",
                report.get("venue"),
                report.get("timeframes"),
                report.get("hits"),
                report.get("approved"),
                report.get("opened"),
                time.perf_counter() - started,
            )
            cycle += 1
            if report.get("opened") or cycle % 3 == 0:
                audit = await asyncio.to_thread(auditor.review_all)
                logger.info("supervisor reviewed=%s opened=%s", audit.get("reviewed"), report.get("opened"))
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001
            logger.warning("agent loop failed: %s", exc)
        # A slow desk must not stack cycles back-to-back and starve the API.
        elapsed = time.perf_counter() - started
        await asyncio.sleep(max(AGENT_MIN_IDLE_SECONDS, AGENT_CYCLE_SECONDS - elapsed))
