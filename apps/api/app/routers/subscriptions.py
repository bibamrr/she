from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select

from apps.api.app.db import get_session
from apps.api.app.models import PaymentSession, User
from apps.api.app.schemas import SubscribeRequest, UserPublic
from apps.api.app.security import get_current_user, get_optional_user
from apps.api.app.services import access, mailer, payments

router = APIRouter(prefix="/api/subscriptions", tags=["subscriptions"])

PLANS = access.PLANS


def _public(user: User) -> UserPublic:
    return UserPublic(
        id=user.id or 0,
        email=user.email,
        display_name=user.display_name,
        locale=user.locale,
        plan=access.plan_of(user)["id"],
        subscription_tier=access.plan_of(user)["id"],
        balance=user.balance,
        email_verified=user.email_verified,
        is_admin=user.is_admin,
        plan_expires_at=user.plan_expires_at.isoformat() if user.plan_expires_at else None,
        entitlements=access.entitlements(user),
        max_charts=access.plan_of(user)["max_charts"],
    )


def _require_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    return user


@router.get("/plans")
def plans() -> dict[str, Any]:
    return {"plans": PLANS, "features": access.FEATURES, "payments": payments.payments_ready()}


@router.get("/entitlements")
def public_entitlements(user: Optional[User] = Depends(get_optional_user)) -> dict[str, Any]:
    return access.access_summary(user)


@router.post("/checkout")
def checkout(
    payload: SubscribeRequest,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    result = payments.create_checkout(user, payload.plan, session)
    if result.get("activated"):
        result["user"] = _public(user).model_dump()
    return result


@router.post("/subscribe")
def subscribe(
    payload: SubscribeRequest,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    """Paid plans open checkout. Explorer still activates immediately."""
    return checkout(payload, user, session)


@router.post("/stripe/webhook")
async def stripe_webhook(request: Request, session: Session = Depends(get_session)) -> dict[str, Any]:
    body = await request.body()
    signature = request.headers.get("stripe-signature", "")
    return payments.fulfill_stripe_event(body, signature, session)


def _test_desk_html(row: PaymentSession, user: Optional[User]) -> str:
    locale = user.locale if user else "ar"
    rtl = "rtl" if locale == "ar" else "ltr"
    title = "دفع تجريبي — SHC" if locale == "ar" else "SHC test checkout"
    plan = row.plan
    amount = f"${row.amount_cents / 100:.0f}"
    action = f"/api/subscriptions/pay/test/{row.token}/confirm"
    pay = "ادفع بالبطاقة التجريبية" if locale == "ar" else "Pay with test card"
    hint = (
        "وضع تجريبي: لا يُخصم مبلغ حقيقي. بعد التأكيد تُفعَّل الباقة فوراً."
        if locale == "ar"
        else "Test desk: no real charge. Confirming activates the plan immediately."
    )
    return f"""<!doctype html><html lang="{locale}" dir="{rtl}"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<style>
body{{margin:0;min-height:100vh;background:#05070a;color:#e8edf4;font-family:"IBM Plex Sans","IBM Plex Sans Arabic",sans-serif;
display:flex;align-items:center;justify-content:center}}
.card{{width:min(420px,92vw);background:#0d131a;border:1px solid #c8a45a;border-radius:12px;padding:28px}}
h1{{margin:0 0 8px;font-size:22px;color:#e8c36a}}
p{{color:#8b98a8;line-height:1.7}}
.big{{font-size:32px;color:#f2d98a;margin:16px 0}}
button{{width:100%;border:0;background:#c8a45a;color:#111;font-weight:700;padding:12px 16px;border-radius:8px;cursor:pointer}}
</style></head><body>
<form class="card" method="post" action="{action}">
<h1>SHC</h1>
<p>{hint}</p>
<p>{plan}</p>
<div class="big">{amount}</div>
<button type="submit">{pay} · 4242</button>
</form></body></html>"""


@router.get("/pay/test/{token}", response_class=HTMLResponse)
def test_pay_page(token: str, session: Session = Depends(get_session)) -> HTMLResponse:
    row = session.exec(select(PaymentSession).where(PaymentSession.token == token)).first()
    if not row or row.provider != "test":
        raise HTTPException(status_code=404, detail="Test checkout not found")
    if row.status == "paid":
        return RedirectResponse("/settings?paid=1", status_code=303)
    user = session.get(User, row.user_id)
    return HTMLResponse(_test_desk_html(row, user))


@router.post("/pay/test/{token}/confirm")
def test_pay_confirm(token: str, session: Session = Depends(get_session)) -> RedirectResponse:
    row = session.exec(select(PaymentSession).where(PaymentSession.token == token)).first()
    if not row or row.provider != "test":
        raise HTTPException(status_code=404, detail="Test checkout not found")
    payments.fulfill_token(token, session)
    return RedirectResponse("/settings?paid=1", status_code=303)


@router.get("/dashboard")
def dashboard(user: User = Depends(get_current_user)) -> dict[str, Any]:
    summary = access.access_summary(user)
    summary["plans"] = PLANS
    summary["payments"] = payments.payments_ready()
    summary["balance"] = user.balance
    summary["display_name"] = user.display_name
    summary["email"] = user.email
    summary["created_at"] = user.created_at.isoformat() if user.created_at else None
    summary["last_login_at"] = user.last_login_at.isoformat() if user.last_login_at else None
    return summary


@router.get("/admin/members")
def admin_members(
    admin: User = Depends(_require_admin),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    users = session.exec(select(User).order_by(User.id)).all()
    return {
        "members": [
            {
                "id": u.id,
                "email": u.email,
                "display_name": u.display_name,
                "plan": u.plan,
                "subscription_tier": access.user_tier(u),
                "effective_plan": access.plan_of(u)["id"],
                "active": access.is_active_subscription(u),
                "days_left": access.days_left(u),
                "email_verified": u.email_verified,
                "is_admin": u.is_admin,
                "balance": u.balance,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in users
        ],
        "outbox": mailer.outbox(),
        "payments": payments.payments_ready(),
    }


@router.post("/admin/set-plan")
def admin_set_plan(
    payload: dict,
    admin: User = Depends(_require_admin),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    email = str(payload.get("email", "")).lower()
    plan_id = str(payload.get("plan", "explorer"))
    target = session.exec(select(User).where(User.email == email)).first()
    if not target:
        raise HTTPException(status_code=404, detail="Member not found")
    access.activate(target, plan_id)
    session.add(target)
    session.commit()
    return {"ok": True, "email": email, "plan": plan_id}
