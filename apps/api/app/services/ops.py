"""Hidden operations-room snapshot for the /admin desk."""

from __future__ import annotations

import hmac
import json
import secrets
import time
from datetime import datetime, timezone
from typing import Any, Optional

from sqlmodel import Session, select

from apps.api.app.config import get_settings
from apps.api.app.models import AgentDesk, AgentReport, AlertDelivery, PaperAccount, PaperPosition, User
from apps.api.app.services import paper
from apps.api.app.services.stables import skip_crypto_hunter

_OPS_TTL = 12 * 3600
_TOKENS: dict[str, float] = {}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def password_ok(password: str) -> bool:
    expected = (get_settings().admin_ops_password or "Binamer123").encode()
    given = (password or "").encode()
    left = hmac.new(b"shc-ops", expected, "sha256").digest()
    right = hmac.new(b"shc-ops", given, "sha256").digest()
    return hmac.compare_digest(left, right)


def issue_token() -> str:
    token = secrets.token_urlsafe(32)
    _TOKENS[token] = time.time() + _OPS_TTL
    for key, exp in list(_TOKENS.items()):
        if exp <= time.time():
            _TOKENS.pop(key, None)
    return token


def token_ok(token: str) -> bool:
    exp = _TOKENS.get(token or "")
    return bool(exp and exp > time.time())


def revoke_token(token: str) -> None:
    _TOKENS.pop(token or "", None)


def _iso(value: Any) -> Optional[str]:
    if value is None:
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def _age_seconds(value: Any) -> Optional[float]:
    if value is None:
        return None
    stamp = value
    if getattr(stamp, "tzinfo", None) is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    return round((_now() - stamp).total_seconds(), 1)


def _parse_body(raw: str) -> dict[str, Any]:
    try:
        data = json.loads(raw or "{}")
        return data if isinstance(data, dict) else {"raw": raw}
    except Exception:
        return {"raw": raw}


def snapshot(session: Session) -> dict[str, Any]:
    desks = session.exec(select(AgentDesk)).all()
    reports = session.exec(select(AgentReport).order_by(AgentReport.id.desc())).all()
    positions = session.exec(select(PaperPosition)).all()
    accounts = session.exec(select(PaperAccount)).all()
    deliveries = session.exec(select(AlertDelivery).order_by(AlertDelivery.id.desc())).all()[:80]
    users = {int(u.id or 0): u for u in session.exec(select(User)).all()}

    from apps.api.app.services import botday

    day = botday.report(session)
    live = day.get("live") or {}
    bot_open = [row for row in positions if row.status == "open" and (row.source or "") == "execution_bot"]
    bot_closed = [row for row in positions if row.status != "open" and (row.source or "") == "execution_bot"]
    wins = int(live.get("wins") or 0)
    losses = int(live.get("losses") or 0)
    decided = wins + losses
    win_rate = round(wins / decided * 100, 1) if decided else None
    realized = float(live.get("realized_pnl") or 0)

    last_tick = max((d.last_tick_at for d in desks if d.last_tick_at), default=None)
    last_audit = max((d.last_audit_at for d in desks if d.last_audit_at), default=None)
    tick_age = _age_seconds(last_tick)
    audit_age = _age_seconds(last_audit)
    exec_live = tick_age is not None and tick_age <= 300
    audit_live = audit_age is not None and audit_age <= 600
    thresholds = [float(d.min_confidence) for d in desks] or [88.0]

    audit_rows = []
    for row in reports:
        if row.kind != "audit":
            continue
        body = _parse_body(row.body)
        correction = body.get("correction") or {}
        hist = body.get("historical") or {}
        user = users.get(int(row.user_id or 0))
        audit_rows.append(
            {
                "id": row.id,
                "at": _iso(row.created_at),
                "user": user.email if user else str(row.user_id),
                "win_rate": body.get("win_rate"),
                "historical_win_rate": hist.get("win_rate") if isinstance(hist, dict) else None,
                "threshold_from": (correction.get("from") if isinstance(correction, dict) else None),
                "threshold_to": (correction.get("to") if isinstance(correction, dict) else None),
                "applied": bool(correction.get("applied")) if isinstance(correction, dict) else False,
                "notes": (correction.get("notes") if isinstance(correction, dict) else []) or body.get("notes") or [],
                "sample": body.get("reviewed") or body.get("bot_trades"),
            }
        )
        if len(audit_rows) >= 24:
            break

    fills = []
    for row in reports:
        if row.kind != "execution":
            continue
        body = _parse_body(row.body)
        user = users.get(int(row.user_id or 0))
        fills.append(
            {
                "id": row.id,
                "at": _iso(row.created_at),
                "user": user.email if user else str(row.user_id),
                "symbol": body.get("symbol"),
                "side": body.get("side"),
                "confidence": body.get("confidence"),
                "entry": body.get("entry"),
                "pnl": None,
            }
        )
        if len(fills) >= 16:
            break

    bank = float(paper.DEFAULT_CASH)
    fleet_cash = round(sum(float(a.cash or 0) for a in accounts), 2)
    fleet_start = round(sum(float(a.starting_cash or bank) for a in accounts), 2)
    books = []
    for acc in accounts:
        user = users.get(int(acc.user_id or 0))
        owned = [row for row in positions if row.user_id == acc.user_id and (row.source or "") != "execution_bot"]
        closed_pnl = sum(float(row.pnl or 0) for row in owned if row.status != "open")
        books.append(
            {
                "user": user.email if user else str(acc.user_id),
                "cash": round(float(acc.cash or 0), 2),
                "starting_cash": round(float(acc.starting_cash or bank), 2),
                "realized_pnl": round(closed_pnl, 4),
                "open": sum(1 for row in owned if row.status == "open"),
            }
        )
    books.sort(key=lambda item: abs(float(item["realized_pnl"])), reverse=True)

    from apps.api.app.routers import system
    from apps.api.app.services.scanner import crypto_universe
    from apps.api.app.services import stocks

    crypto_rows = []
    try:
        crypto_rows = crypto_universe()
    except Exception:
        crypto_rows = []
    blocked = [row for row in crypto_rows if skip_crypto_hunter(row.get("symbol") or "", row)]
    tradeable = len(crypto_rows) - len(blocked)
    diag = system.diagnostics(probe=True)
    providers = (diag.get("stock_providers") or stocks.provider_status())
    venue_status = (providers.get("venues") or {}) if isinstance(providers, dict) else {}
    feeds = {
        "crypto": {
            "ok": bool((diag.get("binance") or {}).get("ok")) or tradeable > 0,
            "symbols": tradeable,
            "latency_ms": (diag.get("binance") or {}).get("latency_ms"),
        },
        "tadawul": venue_status.get("tadawul") or {"ok": False},
        "us": venue_status.get("us") or {"ok": False},
        "europe": venue_status.get("europe") or {"ok": False},
        "asia": venue_status.get("asia") or {"ok": False},
        "commodities": venue_status.get("commodities") or {"ok": False},
    }

    sent_ok = sum(1 for row in deliveries if row.ok)
    sent_fail = sum(1 for row in deliveries if not row.ok)
    hook_rows = []
    for row in deliveries[:36]:
        user = users.get(int(row.user_id or 0))
        hook_rows.append(
            {
                "at": _iso(row.created_at),
                "user": user.email if user else str(row.user_id),
                "channel": row.channel,
                "symbol": row.symbol,
                "ok": bool(row.ok),
                "detail": (row.detail or "")[:120],
            }
        )

    from apps.api.app.services import notify

    return {
        "ok": True,
        "generated_at": _now().isoformat(),
        "bank": bank,
        "agents": {
            "execution": {
                "live": exec_live,
                "last_tick_at": _iso(last_tick),
                "age_seconds": tick_age,
                "desks": len(desks),
                "open_fills": int(live.get("open_now") or len(bot_open)),
                "closed_fills": int(live.get("closed") or 0),
                "win_rate": win_rate,
            },
            "auditor": {
                "live": audit_live,
                "last_audit_at": _iso(last_audit),
                "age_seconds": audit_age,
                "threshold_avg": round(sum(thresholds) / len(thresholds), 1),
                "threshold_min": min(thresholds),
                "threshold_max": max(thresholds),
                "reviews": len(audit_rows),
            },
        },
        "bot_day": day,
        "paper": {
            "unit_bank": bank,
            "accounts": len(accounts),
            "fleet_starting_cash": fleet_start,
            "fleet_cash": fleet_cash,
            "bot_realized_pnl": realized,
            "bot_open": int(live.get("open_now") or 0),
            "bot_closed": int(live.get("closed") or 0),
            "win_rate": win_rate,
            "wins": wins,
            "losses": losses,
            "books": books[:12],
        },
        "audit": audit_rows,
        "fills": fills,
        "feeds": feeds,
        "filters": {
            "crypto_listed": len(crypto_rows),
            "stables_blocked": len(blocked),
            "tradeable": tradeable,
            "blocked_sample": [row.get("symbol") for row in blocked[:8]],
        },
        "hooks": {
            "telegram_configured": bool(get_settings().telegram_bot_token.strip()),
            "delivered_ok": sent_ok,
            "failed": sent_fail,
            "recent": hook_rows,
            "memory_outbox": notify.outbox()[:12],
        },
        "system": {
            "uptime_seconds": diag.get("uptime_seconds"),
            "memory_rss_mb": diag.get("memory_rss_mb"),
            "binance": diag.get("binance"),
        },
    }
