from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from backend.app.db import get_session
from backend.app.deps import get_current_user
from backend.app.models import Plan, PlanCode, User

router = APIRouter(prefix="/billing", tags=["billing"])


class SubscribeBody(BaseModel):
    plan: PlanCode
    deposit: float = 0


@router.get("/plans")
def list_plans(session: Session = Depends(get_session)) -> list[dict]:
    plans = session.exec(select(Plan)).all()
    return [
        {
            "code": p.code,
            "name_en": p.name_en,
            "name_ar": p.name_ar,
            "monthly_price": p.monthly_price,
            "credits_per_month": p.credits_per_month,
            "max_watchlist": p.max_watchlist,
        }
        for p in plans
    ]


@router.post("/subscribe")
def subscribe(
    body: SubscribeBody,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict:
    plan = session.exec(select(Plan).where(Plan.code == body.plan.value)).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    user.plan = plan.code
    user.credits = plan.credits_per_month
    if body.deposit > 0:
        user.balance += body.deposit
    session.add(user)
    session.commit()
    session.refresh(user)
    return {
        "plan": user.plan,
        "credits": user.credits,
        "balance": user.balance,
    }
