"""Checkout + fulfillment. Stripe when keys exist, otherwise a local test desk."""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import secrets
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import HTTPException
from sqlmodel import Session, select

from apps.api.app.config import get_settings
from apps.api.app.models import PaymentSession, User
from apps.api.app.services import access, mailer

logger = logging.getLogger("shc.payments")

STRIPE_API = "https://api.stripe.com/v1/checkout/sessions"


def provider_name() -> str:
    return "stripe" if get_settings().stripe_secret_key.strip() else "test"


def payments_ready() -> dict[str, Any]:
    name = provider_name()
    settings = get_settings()
    return {
        "provider": name,
        "ready": True,
        "test_mode": name == "test" or settings.stripe_secret_key.startswith("sk_test_"),
        "webhook_configured": bool(settings.stripe_webhook_secret.strip()),
    }


def _amount_cents(plan: dict[str, Any]) -> int:
    return int(round(float(plan.get("price") or 0) * 100))


def _new_session(user: User, plan: dict[str, Any], provider: str) -> PaymentSession:
    return PaymentSession(
        token=secrets.token_urlsafe(24),
        user_id=int(user.id or 0),
        plan=plan["id"],
        amount_cents=_amount_cents(plan),
        currency="usd",
        provider=provider,
        status="pending",
    )


def _stripe_checkout(user: User, plan: dict[str, Any], token: str) -> tuple[str, str]:
    settings = get_settings()
    base = settings.public_base_url.rstrip("/")
    name = plan.get("name_en") or plan["id"]
    fields = {
        "mode": "payment",
        "success_url": f"{base}/settings?paid=1",
        "cancel_url": f"{base}/settings?canceled=1",
        "client_reference_id": token,
        "customer_email": user.email,
        "metadata[token]": token,
        "metadata[user_id]": str(user.id),
        "metadata[plan]": plan["id"],
        "line_items[0][quantity]": "1",
        "line_items[0][price_data][currency]": "usd",
        "line_items[0][price_data][unit_amount]": str(_amount_cents(plan)),
        "line_items[0][price_data][product_data][name]": f"SHC {name}",
        "line_items[0][price_data][product_data][description]": plan.get("tagline_en") or plan["id"],
    }
    request = urllib.request.Request(
        STRIPE_API,
        data=urllib.parse.urlencode(fields).encode(),
        headers={
            "Authorization": f"Bearer {settings.stripe_secret_key.strip()}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="ignore")
        logger.warning("stripe checkout failed: %s %s", exc.code, detail)
        raise HTTPException(status_code=502, detail="Stripe checkout failed") from exc
    url = payload.get("url")
    session_id = payload.get("id")
    if not url or not session_id:
        raise HTTPException(status_code=502, detail="Stripe returned no checkout URL")
    return str(url), str(session_id)


def create_checkout(user: User, plan_id: str, session: Session) -> dict[str, Any]:
    tier = access.normalize_tier(plan_id)
    plan = access.PLAN_INDEX.get(tier)
    if not plan:
        raise HTTPException(status_code=400, detail="Unknown plan")
    if tier == access.EXPLORER:
        access.activate(user, access.EXPLORER)
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"activated": True, "provider": "free", "plan": access.EXPLORER, "checkout_url": None}

    row = _new_session(user, plan, provider_name())
    if row.provider == "stripe":
        url, ref = _stripe_checkout(user, plan, row.token)
        row.provider_ref = ref
    else:
        url = f"{get_settings().public_base_url.rstrip('/')}/api/subscriptions/pay/test/{row.token}"
    session.add(row)
    session.commit()
    session.refresh(row)
    return {
        "activated": False,
        "provider": row.provider,
        "plan": plan["id"],
        "checkout_url": url,
        "session_token": row.token,
        "amount_cents": row.amount_cents,
        "currency": row.currency,
    }


def fulfill_token(token: str, session: Session, expected_user_id: Optional[int] = None) -> PaymentSession:
    row = session.exec(select(PaymentSession).where(PaymentSession.token == token)).first()
    if not row:
        raise HTTPException(status_code=404, detail="Payment session not found")
    if expected_user_id is not None and row.user_id != expected_user_id:
        raise HTTPException(status_code=403, detail="Payment session mismatch")
    if row.status == "paid":
        return row
    user = session.get(User, row.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Member not found")
    plan = access.activate(user, row.plan)
    row.status = "paid"
    row.paid_at = datetime.now(timezone.utc)
    session.add(user)
    session.add(row)
    session.commit()
    session.refresh(row)
    expires = user.plan_expires_at.strftime("%Y-%m-%d") if user.plan_expires_at else "—"
    mailer.send_subscription(user.email, user.display_name, user.locale, plan["id"], expires)
    logger.info("fulfilled %s → %s via %s", user.email, plan["id"], row.provider)
    return row


def verify_stripe_signature(payload: bytes, header: str, secret: str, tolerance: int = 300) -> None:
    parts: dict[str, list[str]] = {}
    for item in (header or "").split(","):
        key, _, value = item.partition("=")
        if key and value:
            parts.setdefault(key.strip(), []).append(value.strip())
    timestamp = (parts.get("t") or [None])[0]
    signatures = parts.get("v1") or []
    if not timestamp or not signatures:
        raise HTTPException(status_code=400, detail="Invalid Stripe signature header")
    try:
        if abs(time.time() - int(timestamp)) > tolerance:
            raise HTTPException(status_code=400, detail="Stale Stripe signature")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid Stripe timestamp") from exc
    expected = hmac.new(secret.encode(), f"{timestamp}.".encode() + payload, hashlib.sha256).hexdigest()
    if not any(hmac.compare_digest(expected, sig) for sig in signatures):
        raise HTTPException(status_code=400, detail="Stripe signature mismatch")


def fulfill_stripe_event(payload: bytes, signature: str, session: Session) -> dict[str, Any]:
    settings = get_settings()
    secret = settings.stripe_webhook_secret.strip()
    if not secret:
        raise HTTPException(status_code=503, detail="SHC_STRIPE_WEBHOOK_SECRET is not set")
    verify_stripe_signature(payload, signature, secret)
    try:
        event = json.loads(payload.decode())
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="Invalid Stripe payload") from exc
    kind = event.get("type") or ""
    if kind not in {"checkout.session.completed", "checkout.session.async_payment_succeeded"}:
        return {"ok": True, "ignored": kind}
    data = (event.get("data") or {}).get("object") or {}
    if data.get("payment_status") not in {None, "paid", "no_payment_required"}:
        if data.get("status") != "complete":
            return {"ok": True, "ignored": "unpaid"}
    token = ((data.get("metadata") or {}).get("token")) or data.get("client_reference_id")
    if not token:
        raise HTTPException(status_code=400, detail="Stripe session missing SHC token")
    row = fulfill_token(str(token), session)
    if data.get("id") and not row.provider_ref:
        row.provider_ref = str(data["id"])
        session.add(row)
        session.commit()
    return {"ok": True, "plan": row.plan, "status": row.status}
