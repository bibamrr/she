"""Outbound Hunter alerts: HTTPS webhook, Telegram Bot API, email."""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

from sqlmodel import Session, select

from apps.api.app.config import get_settings
from apps.api.app.db import engine
from apps.api.app.models import AlertDelivery, User
from apps.api.app.services import access, mailer
from apps.api.app.services.hunter import hunt, is_launchable
from apps.api.app.services.stables import is_stablecoin

logger = logging.getLogger("shc.notify")

_OUTBOX: list[dict[str, Any]] = []
_OUTBOX_MAX = 80


def outbox() -> list[dict[str, Any]]:
    return list(reversed(_OUTBOX))


def _record(entry: dict[str, Any]) -> None:
    _OUTBOX.append(entry)
    while len(_OUTBOX) > _OUTBOX_MAX:
        _OUTBOX.pop(0)


def webhook_allowed(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme == "https" and parsed.netloc:
        return True
    host = (parsed.hostname or "").lower()
    return parsed.scheme == "http" and host in {"127.0.0.1", "localhost"}


def _post_json(url: str, payload: dict[str, Any], timeout: int = 12) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "SHC-Alerts/1.0"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read()[:400]
        return {"ok": True, "status": response.status, "detail": body.decode(errors="ignore")}


def send_webhook(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    try:
        return _post_json(url, payload)
    except Exception as exc:  # noqa: BLE001
        logger.warning("webhook failed %s: %s", url, exc)
        return {"ok": False, "error": str(exc)}


def send_telegram(chat_id: str, text: str) -> dict[str, Any]:
    token = get_settings().telegram_bot_token.strip()
    if not token:
        return {"ok": False, "error": "SHC_TELEGRAM_BOT_TOKEN is not set"}
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    fields = {"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": "true"}
    request = urllib.request.Request(
        url,
        data=urllib.parse.urlencode(fields).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            payload = json.loads(response.read().decode())
        if not payload.get("ok"):
            return {"ok": False, "error": str(payload.get("description") or payload)}
        return {"ok": True, "message_id": (payload.get("result") or {}).get("message_id")}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="ignore")
        logger.warning("telegram failed: %s %s", exc.code, detail)
        return {"ok": False, "error": detail or str(exc)}
    except Exception as exc:  # noqa: BLE001
        logger.warning("telegram failed: %s", exc)
        return {"ok": False, "error": str(exc)}


def _already_sent(session: Session, user_id: int, dedupe_key: str, channel: str) -> bool:
    row = session.exec(
        select(AlertDelivery).where(
            AlertDelivery.user_id == user_id,
            AlertDelivery.dedupe_key == dedupe_key,
            AlertDelivery.channel == channel,
            AlertDelivery.ok == True,  # noqa: E712
        )
    ).first()
    return row is not None


def _store(session: Session, user_id: int, dedupe_key: str, symbol: str, timeframe: str, channel: str, result: dict[str, Any]) -> None:
    ok = bool(result.get("ok"))
    detail = str(result.get("error") or result.get("detail") or result.get("status") or "")[:400]
    session.add(
        AlertDelivery(
            user_id=user_id,
            dedupe_key=dedupe_key,
            symbol=symbol,
            timeframe=timeframe,
            channel=channel,
            ok=ok,
            detail=detail,
        )
    )
    _record(
        {
            "at": datetime.now(timezone.utc).isoformat(),
            "user_id": user_id,
            "symbol": symbol,
            "timeframe": timeframe,
            "channel": channel,
            "ok": ok,
            "detail": detail,
        }
    )


def _telegram_text(payload: dict[str, Any], locale: str) -> str:
    side = payload.get("side") or "neutral"
    arrow = "▲" if side == "bullish" else "▼" if side == "bearish" else "●"
    if locale == "ar":
        return (
            f"<b>SHC · إشارة نخبة</b>\n"
            f"{arrow} {payload.get('symbol')} · {payload.get('timeframe')}\n"
            f"{payload.get('label') or side} · ثقة {payload.get('confidence')}%\n"
            f"السعر {payload.get('last_price') or '—'}"
        )
    return (
        f"<b>SHC elite signal</b>\n"
        f"{arrow} {payload.get('symbol')} · {payload.get('timeframe')}\n"
        f"{payload.get('label') or side} · {payload.get('confidence')}%\n"
        f"price {payload.get('last_price') or '—'}"
    )


def normalize_hit(hit: dict[str, Any], timeframe: str = "15m") -> dict[str, Any]:
    signal = hit.get("signal") or {}
    side = signal.get("side") or ("bullish" if "bull" in str(hit.get("state") or "") else "bearish" if "bear" in str(hit.get("state") or "") else "neutral")
    return {
        "product": "SHC",
        "kind": "hunter_elite",
        "symbol": hit.get("symbol"),
        "timeframe": hit.get("timeframe") or timeframe,
        "side": side,
        "label": signal.get("label") or hit.get("state") or "elite",
        "confidence": hit.get("confidence") or signal.get("confidence"),
        "last_price": hit.get("last_price"),
        "time": signal.get("time") or hit.get("time"),
        "state": hit.get("state"),
        "volume_ratio": hit.get("volume_ratio"),
    }


def dispatch_user(session: Session, user: User, payload: dict[str, Any]) -> dict[str, Any]:
    dedupe = f"{payload.get('symbol')}|{payload.get('timeframe')}|{payload.get('time')}|{payload.get('confidence')}"
    results: dict[str, Any] = {}
    symbol = str(payload.get("symbol") or "")
    timeframe = str(payload.get("timeframe") or "")

    if user.webhook_url and access.has_feature(user, "webhooks"):
        if not _already_sent(session, int(user.id or 0), dedupe, "webhook"):
            result = send_webhook(user.webhook_url, payload)
            _store(session, int(user.id or 0), dedupe, symbol, timeframe, "webhook", result)
            results["webhook"] = result
        else:
            results["webhook"] = {"ok": True, "deduped": True}

    if user.telegram_chat_id and access.has_feature(user, "telegram"):
        if not _already_sent(session, int(user.id or 0), dedupe, "telegram"):
            result = send_telegram(user.telegram_chat_id, _telegram_text(payload, user.locale))
            _store(session, int(user.id or 0), dedupe, symbol, timeframe, "telegram", result)
            results["telegram"] = result
        else:
            results["telegram"] = {"ok": True, "deduped": True}

    if access.has_feature(user, "telegram"):
        if not _already_sent(session, int(user.id or 0), dedupe, "email"):
            result = mailer.send_alert(user.email, user.display_name, user.locale, payload)
            _store(session, int(user.id or 0), dedupe, symbol, timeframe, "email", result)
            results["email"] = result
        else:
            results["email"] = {"ok": True, "deduped": True}

    session.commit()
    return results


def dispatch_hit_to_subscribers(hit: dict[str, Any]) -> int:
    if is_stablecoin(str(hit.get("symbol") or "")):
        return 0
    if not is_launchable(hit, float(get_settings().alert_min_confidence)):
        return 0
    payload = normalize_hit(hit)
    if float(payload.get("confidence") or 0) < float(get_settings().alert_min_confidence):
        return 0
    sent = 0
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        for user in users:
            if not access.has_feature(user, "alerts") and not access.has_feature(user, "webhooks"):
                continue
            if not user.webhook_url and not user.telegram_chat_id and not access.has_feature(user, "telegram"):
                continue
            results = dispatch_user(session, user, payload)
            if any(item.get("ok") and not item.get("deduped") for item in results.values()):
                sent += 1
    return sent


def scan_and_dispatch(timeframe: str = "15m") -> dict[str, Any]:
    data = hunt(timeframe, 16, float(get_settings().alert_min_confidence), 2.0)
    floor = float(get_settings().alert_min_confidence)
    elite = [hit for hit in (data.get("elite") or []) if is_launchable(hit, floor) and not is_stablecoin(str(hit.get("symbol") or ""))]
    delivered = 0
    for hit in elite:
        delivered += dispatch_hit_to_subscribers(hit)
    return {"scanned": data.get("scanned"), "elite": len(elite), "delivered": delivered}


def test_payload(user: User) -> dict[str, Any]:
    return {
        "product": "SHC",
        "kind": "test",
        "symbol": "BTC/USDT",
        "timeframe": "15m",
        "side": "bullish",
        "label": "test_alert",
        "confidence": 91.0,
        "last_price": 0,
        "time": int(datetime.now(timezone.utc).timestamp()),
        "user": user.email,
    }
