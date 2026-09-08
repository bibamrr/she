from __future__ import annotations

import asyncio
import logging
from typing import Any, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

from apps.api.app.config import get_settings
from apps.api.app.db import get_session
from apps.api.app.models import User
from apps.api.app.services import access, notify
from apps.api.app.services.hunter import match_official

logger = logging.getLogger("shc.alerts")

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


class EmitPayload(BaseModel):
    symbol: str
    timeframe: str = "15m"
    side: str = "bullish"
    label: str = "elite"
    confidence: float = 90.0
    last_price: Optional[float] = None
    time: Optional[int] = None
    state: str = ""


@router.post("/emit")
def emit(
    payload: EmitPayload,
    user: User = Depends(access.require_any("alerts", "webhooks", "telegram")),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    official = match_official(payload.model_dump(), float(get_settings().alert_min_confidence))
    if not official:
        return {"ok": False, "skipped": "not_hunter", "channels": {}}
    return {"ok": True, "channels": notify.dispatch_user(session, user, notify.normalize_hit(official))}


@router.post("/test")
def test_alert(
    user: User = Depends(access.require_any("alerts", "webhooks", "telegram")),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    return {"ok": True, "channels": notify.dispatch_user(session, user, notify.test_payload(user))}


@router.get("/outbox")
def alert_outbox(user: User = Depends(access.require_any("alerts", "webhooks", "telegram"))) -> dict[str, Any]:
    rows = notify.outbox()
    if not user.is_admin:
        rows = [row for row in rows if row.get("user_id") == user.id]
    return {"deliveries": rows[:40], "bot_configured": bool(get_settings().telegram_bot_token.strip())}


async def alert_loop() -> None:
    settings = get_settings()
    interval = max(30, int(settings.alert_scan_seconds or 60))
    await asyncio.sleep(20)
    while True:
        try:
            report = await asyncio.to_thread(notify.scan_and_dispatch)
            if report.get("elite"):
                logger.info("alert scan elite=%s delivered=%s", report.get("elite"), report.get("delivered"))
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001
            logger.warning("alert scan failed: %s", exc)
        await asyncio.sleep(interval)
