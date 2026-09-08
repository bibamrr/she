"""Shared agent desk state. Threshold writes belong to the auditor only."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Optional

from sqlmodel import Session, select

from apps.api.app.models import AgentDesk, AgentReport, User
from apps.api.app.services import paper

DESKS = ("crypto", "tadawul", "us", "europe", "asia", "commodities")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def params_of(desk: AgentDesk) -> dict[str, Any]:
    try:
        data = json.loads(desk.params_json or "{}")
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def get_desk(session: Session, user: User) -> AgentDesk:
    desk = session.exec(select(AgentDesk).where(AgentDesk.user_id == user.id)).first()
    if desk:
        changed = False
        if not desk.execution_enabled:
            desk.execution_enabled = True
            changed = True
        if (desk.venue or "") not in ("", "auto") and desk.venue not in DESKS:
            desk.venue = "auto"
            changed = True
        if changed:
            desk.updated_at = _now()
            session.add(desk)
            session.commit()
            session.refresh(desk)
        return desk
    desk = AgentDesk(user_id=int(user.id or 0), execution_enabled=True, venue="auto", updated_at=_now())
    session.add(desk)
    session.commit()
    session.refresh(desk)
    return desk


def serialize_desk(desk: AgentDesk) -> dict[str, Any]:
    return {
        "execution_enabled": bool(desk.execution_enabled),
        "min_confidence": float(desk.min_confidence),
        "max_open": int(desk.max_open),
        "risk_pct": float(desk.risk_pct),
        "venue": desk.venue or "auto",
        "last_tick_at": desk.last_tick_at.isoformat() if desk.last_tick_at else None,
        "last_audit_at": desk.last_audit_at.isoformat() if desk.last_audit_at else None,
        "params": params_of(desk),
        "starting_cash": paper.DEFAULT_CASH,
    }


def save_runtime(
    session: Session,
    user: User,
    venue: Optional[str] = None,
    max_open: Optional[int] = None,
    risk_pct: Optional[float] = None,
) -> AgentDesk:
    """Execution-safe desk updates. Never touches min_confidence."""
    desk = get_desk(session, user)
    desk.execution_enabled = True
    if venue is not None:
        key = (venue or "auto").strip().lower()
        desk.venue = key if key in DESKS or key == "auto" else "auto"
    if max_open is not None:
        desk.max_open = max(1, min(12, int(max_open)))
    # Bot sizing is autonomous — subscriber risk_pct is never applied to fills.
    _ = risk_pct
    desk.updated_at = _now()
    session.add(desk)
    session.commit()
    session.refresh(desk)
    return desk


def apply_threshold(session: Session, desk: AgentDesk, value: float) -> float:
    """Auditor-only write path for the confidence threshold."""
    next_value = round(max(75.0, min(96.0, float(value))), 1)
    desk.min_confidence = next_value
    desk.updated_at = _now()
    session.add(desk)
    return next_value


def write_report(session: Session, user: User, kind: str, title: str, body: dict[str, Any]) -> AgentReport:
    row = AgentReport(
        user_id=int(user.id or 0),
        kind=kind,
        title=title,
        body=json.dumps(body, ensure_ascii=False, default=str),
        created_at=_now(),
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return row


def list_reports(session: Session, user: User, kind: str = "", limit: int = 20) -> list[dict[str, Any]]:
    stmt = select(AgentReport).where(AgentReport.user_id == user.id)
    if kind:
        stmt = stmt.where(AgentReport.kind == kind)
    rows = session.exec(stmt.order_by(AgentReport.id.desc())).all()[:limit]
    out = []
    for row in rows:
        try:
            payload = json.loads(row.body or "{}")
        except Exception:
            payload = {"raw": row.body}
        out.append(
            {
                "id": row.id,
                "kind": row.kind,
                "title": row.title,
                "created_at": row.created_at.isoformat() if row.created_at else None,
                "payload": payload,
            }
        )
    return out
