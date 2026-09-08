from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from apps.api.app.models import User
from apps.api.app.services import access, assistant

router = APIRouter(prefix="/api/assistant", tags=["assistant"])


class AskRequest(BaseModel):
    question: str
    symbol: str = "BTC/USDT"
    timeframe: str = "15m"
    locale: str = "ar"


@router.post("/ask")
def ask(
    payload: AskRequest,
    _user: User = Depends(access.require_feature("assistant")),
) -> dict[str, Any]:
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Empty question")
    return assistant.ask(question, payload.symbol, payload.timeframe, payload.locale)


@router.get("/suggestions")
def suggestions(locale: str = "ar") -> dict[str, Any]:
    if locale == "ar":
        items = [
            "ما حالة الاحتقان على العملة الحالية؟",
            "ماذا رصد الصياد الآن؟",
            "ما نسبة نجاح إشارات هذه العملة؟",
            "اشرح لي معنى الثقة 90%+",
            "هل الفريمات متوافقة على الاختراق؟",
        ]
    else:
        items = [
            "What is the compression state right now?",
            "What did the Hunter find?",
            "What is the win rate for this symbol?",
            "Explain what 90%+ confidence means",
            "Are the timeframes aligned for a breakout?",
        ]
    return {"suggestions": items}
