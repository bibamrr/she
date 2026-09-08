from __future__ import annotations

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from apps.api.app.db import get_session
from apps.api.app.models import User
from apps.api.app.security import get_current_user
from apps.api.app.services import watchlist

router = APIRouter(prefix="/api/watchlist", tags=["watchlist"])


class WatchPayload(BaseModel):
    symbols: List[str] = []


class WatchSymbol(BaseModel):
    symbol: str


@router.get("")
def get_watch(user: User = Depends(get_current_user), session: Session = Depends(get_session)) -> dict[str, Any]:
    return watchlist.payload(session, user)


@router.put("")
def put_watch(
    payload: WatchPayload,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    watchlist.replace(session, user, payload.symbols)
    return watchlist.payload(session, user)


@router.post("")
def add_watch(
    payload: WatchSymbol,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    try:
        watchlist.add(session, user, payload.symbol)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return watchlist.payload(session, user)


@router.delete("/{symbol:path}")
def del_watch(
    symbol: str,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    watchlist.remove(session, user, symbol)
    return watchlist.payload(session, user)
