from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from apps.api.app.db import get_session
from apps.api.app.models import User
from apps.api.app.config import get_settings
from apps.api.app.services import access, mailer, notify

router = APIRouter(prefix="/api/integrations", tags=["integrations"])


class WebhookPayload(BaseModel):
    url: str = ""


class TelegramPayload(BaseModel):
    chat_id: str = ""


@router.get("/me")
def status(user: User = Depends(access.require_any("webhooks", "telegram", "alerts"))) -> dict[str, Any]:
    return {
        "webhook_url": user.webhook_url,
        "telegram_chat_id": user.telegram_chat_id,
        "tier": access.user_tier(user),
        "bot_configured": bool(get_settings().telegram_bot_token.strip()),
    }


@router.post("/webhook")
def save_webhook(
    payload: WebhookPayload,
    user: User = Depends(access.require_feature("webhooks")),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    url = payload.url.strip()
    if url and not notify.webhook_allowed(url):
        raise HTTPException(status_code=400, detail="Webhook must be https:// (or http://127.0.0.1 for local test)")
    user.webhook_url = url
    session.add(user)
    session.commit()
    return {"ok": True, "webhook_url": url}


@router.post("/telegram")
def save_telegram(
    payload: TelegramPayload,
    user: User = Depends(access.require_feature("telegram")),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    user.telegram_chat_id = payload.chat_id.strip()
    session.add(user)
    session.commit()
    return {"ok": True, "telegram_chat_id": user.telegram_chat_id}


@router.post("/test-email")
def test_email(user: User = Depends(access.require_feature("telegram"))) -> dict[str, Any]:
    return mailer.send_email(
        user.email,
        "SHC alert test",
        "<p>Elite Brain instant alert channel is live.</p>",
        "Elite Brain instant alert channel is live.",
    )


@router.post("/test-alert")
def test_alert(
    user: User = Depends(access.require_any("webhooks", "telegram", "alerts")),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    return {"ok": True, "channels": notify.dispatch_user(session, user, notify.test_payload(user))}
