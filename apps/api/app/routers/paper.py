from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from apps.api.app.db import get_session
from apps.api.app.models import User
from apps.api.app.security import get_current_user
from apps.api.app.services import paper

router = APIRouter(prefix="/api/paper", tags=["paper"])


class OpenPayload(BaseModel):
    symbol: str
    side: str = "long"
    qty: float
    entry: float
    stop: float = 0
    target: float = 0
    wallet: Optional[float] = None


class ClosePayload(BaseModel):
    exit: Optional[float] = None


class MarkPayload(BaseModel):
    symbol: str
    last: float


class ResetPayload(BaseModel):
    cash: Optional[float] = None


@router.get("/book")
def get_book(user: User = Depends(get_current_user), session: Session = Depends(get_session)) -> dict[str, Any]:
    return paper.book(session, user, scope="manual")


@router.post("/open")
def open_trade(
    payload: OpenPayload,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    try:
        return paper.open_trade(
            session,
            user,
            payload.symbol,
            payload.side,
            payload.qty,
            payload.entry,
            payload.stop,
            payload.target,
            None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/close/{position_id}")
def close_trade(
    position_id: int,
    payload: ClosePayload = ClosePayload(),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    try:
        return paper.close_trade(session, user, position_id, payload.exit)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/mark")
def mark(
    payload: MarkPayload,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    try:
        return paper.mark_symbol(session, user, payload.symbol, payload.last, scope="manual")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/reset")
def reset(
    payload: ResetPayload = ResetPayload(),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    return paper.reset_book(session, user, payload.cash)
