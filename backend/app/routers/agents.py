from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from backend.app.db import get_session
from backend.app.deps import get_current_user
from backend.app.models import User
from backend.app.services.analysis import run_swarm
from backend.app.services.market import fetch_ohlcv, fetch_order_book

router = APIRouter(prefix="/agents", tags=["agents"])

CREDIT_COST = 1


@router.post("/analyze")
def analyze(
    symbol: str = Query("BTCUSDT"),
    timeframe: str = Query("1h"),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict:
    if user.credits < CREDIT_COST:
        raise HTTPException(status_code=402, detail="Insufficient credits")
    candles = fetch_ohlcv(symbol, timeframe=timeframe, limit=300)
    try:
        book = fetch_order_book(symbol, limit=20)
    except Exception:
        book = None
    try:
        result = run_swarm(candles, book)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    user.credits -= CREDIT_COST
    session.add(user)
    session.commit()
    session.refresh(user)
    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "credits_remaining": user.credits,
        **result,
    }
