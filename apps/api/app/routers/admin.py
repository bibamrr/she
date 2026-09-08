from __future__ import annotations

from collections import Counter
from typing import Any, Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from apps.api.app.db import get_session
from apps.api.app.models import User
from apps.api.app.security import get_current_user, get_optional_user
from apps.api.app.services import access, ops
from apps.api.app.routers import system

router = APIRouter(prefix="/api/admin", tags=["admin"])


class UnlockPayload(BaseModel):
    password: str = ""


def _require_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    return user


def _require_ops(
    x_admin_ops: Optional[str] = Header(default=None, alias="X-Admin-Ops"),
    user: Optional[User] = Depends(get_optional_user),
) -> str:
    token = (x_admin_ops or "").strip()
    if ops.token_ok(token):
        return token
    if user and user.is_admin:
        return "admin-session"
    raise HTTPException(status_code=401, detail="locked")


@router.get("/command")
def command_center(
    admin: User = Depends(_require_admin),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    users = session.exec(select(User)).all()
    tiers = Counter(access.plan_of(u)["id"] for u in users)
    active = sum(1 for u in users if access.is_active_subscription(u))
    paid = sum(1 for u in users if access.user_tier(u) != access.EXPLORER and access.is_active_subscription(u))
    diag = system.diagnostics(probe=True)
    hist = system.history()
    return {
        "ok": True,
        "operator": admin.email,
        "members_total": len(users),
        "members_active": active,
        "paid_active": paid,
        "by_tier": {
            "explorer": tiers.get("explorer", 0),
            "pro_hunter": tiers.get("pro_hunter", 0),
            "elite_brain": tiers.get("elite_brain", 0),
        },
        "verified": sum(1 for u in users if u.email_verified),
        "admins": sum(1 for u in users if u.is_admin),
        "diagnostics": diag,
        "history": hist,
        "websocket": {
            "binance_ok": bool((diag.get("binance") or {}).get("ok")),
            "binance_latency_ms": (diag.get("binance") or {}).get("latency_ms"),
            "upstream_avg_ms": hist.get("avg_upstream_latency_ms"),
            "leak_suspected": hist.get("leak_suspected"),
        },
        "recent": [
            {
                "email": u.email,
                "tier": access.plan_of(u)["id"],
                "active": access.is_active_subscription(u),
                "last_login_at": u.last_login_at.isoformat() if u.last_login_at else None,
            }
            for u in sorted(users, key=lambda item: item.id or 0, reverse=True)[:12]
        ],
    }


@router.post("/ops/unlock")
def ops_unlock(payload: UnlockPayload) -> dict[str, Any]:
    if not ops.password_ok(payload.password):
        raise HTTPException(status_code=403, detail="locked")
    return {"ok": True, "token": ops.issue_token(), "ttl_hours": 12}


@router.post("/ops/lock")
def ops_lock(token: str = Depends(_require_ops)) -> dict[str, Any]:
    ops.revoke_token(token)
    return {"ok": True}


@router.get("/ops")
def ops_room(
    token: str = Depends(_require_ops),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    _ = token
    return ops.snapshot(session)
