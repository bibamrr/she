"""Auditor: performance review and threshold correction. Never opens or closes trades."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Optional

from sqlmodel import Session, select

from apps.api.app.db import engine
from apps.api.app.models import AgentReport, PaperPosition, User
from apps.api.app.services import desk as agent_desk
from apps.api.app.services import paper
from apps.api.app.services import swarm
from apps.api.app.services.hunter import backtest

AGENT_KEYS = (
    "hunter",
    "radar_agent",
    "quant_agent",
    "pattern_agent",
    "liquidity_agent",
    "news_sentiment_agent",
    "risk_management_agent",
    "market_sentiment_agent",
    "on_chain_agent",
    "execution",
)

_AGENT_ALIASES = {
    "Radar": "radar_agent",
    "Quant": "quant_agent",
    "Patterns": "pattern_agent",
    "Liquidity": "liquidity_agent",
    "News_Sentiment": "news_sentiment_agent",
    "Risk_Management": "risk_management_agent",
    "Market_Sentiment": "market_sentiment_agent",
    "On_Chain": "on_chain_agent",
}

REVIEW_SOURCES = {"execution_bot", "subscriber"}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _closed_rows(session: Session, user: User) -> list[PaperPosition]:
    rows = session.exec(
        select(PaperPosition)
        .where(PaperPosition.user_id == user.id, PaperPosition.status != "open")
        .order_by(PaperPosition.id.desc())
    ).all()
    return [row for row in rows if (row.source or "") in REVIEW_SOURCES]


def _outcome(row: PaperPosition) -> str:
    if row.reason == "tp" or float(row.pnl or 0) > 0:
        return "win"
    if row.reason == "sl" or float(row.pnl or 0) < 0:
        return "loss"
    return "flat"


def observe_fill(session: Session, user: User, report: dict[str, Any]) -> dict[str, Any]:
    """Immediate handoff: a bot fill is sent to the auditor to prove hunter + execution + paper."""
    desk = agent_desk.get_desk(session, user)
    book = paper.book(session, user, scope="bot")
    payload = {
        "agent": "auditor",
        "kind": "handoff",
        "hunter": "ok",
        "execution": "ok",
        "paper": "ok",
        "sizing": "autonomous",
        "fill": {
            "symbol": report.get("symbol"),
            "side": report.get("side"),
            "entry": report.get("entry"),
            "stop": report.get("stop"),
            "target": report.get("target"),
            "qty": report.get("qty"),
            "notional": report.get("notional")
            or round(float(report.get("qty") or 0) * float(report.get("entry") or 0), 4),
            "confidence": report.get("confidence"),
            "timeframe": report.get("timeframe"),
            "venue": report.get("venue"),
            "position_id": report.get("position_id"),
        },
        "book": {
            "cash": book.get("cash"),
            "equity": book.get("equity"),
            "open": len(book.get("open") or []),
        },
        "reviewed_at": _now().isoformat(),
    }
    agent_desk.write_report(session, user, "audit", f"handoff {report.get('symbol') or ''}".strip(), payload)
    desk.last_audit_at = _now()
    session.add(desk)
    session.commit()
    return payload


def _swarm(session: Session, user: User, desk: Any, bot_rows: list[PaperPosition]) -> dict[str, Any]:
    bot_open = session.exec(
        select(PaperPosition).where(
            PaperPosition.user_id == user.id,
            PaperPosition.status == "open",
            PaperPosition.source == "execution_bot",
        )
    ).all()
    exec_reports = agent_desk.list_reports(session, user, "execution", 6)
    hunter_ok = bool(desk.last_tick_at) or bool(exec_reports)
    execution_ok = bool(bot_open) or bool(bot_rows) or bool(exec_reports)
    notes = []
    if not hunter_ok:
        notes.append("hunter_idle")
    if hunter_ok and not execution_ok:
        notes.append("execution_waiting_for_swarm")
    if execution_ok:
        notes.append("execution_handoff_ok")
    return {
        "hunter": {"ok": hunter_ok, "last_tick_at": desk.last_tick_at.isoformat() if desk.last_tick_at else None},
        "execution": {
            "ok": execution_ok,
            "open": len(bot_open),
            "closed": len(bot_rows),
            "last_fills": [
                {"symbol": row.get("payload", {}).get("symbol"), "timeframe": row.get("payload", {}).get("timeframe")}
                for row in exec_reports[:4]
            ],
        },
        "paper": {"ok": True, "starting_cash": paper.DEFAULT_CASH},
        "sizing": "autonomous",
        "notes": notes,
    }


def _blank_score() -> dict[str, Any]:
    return {"errors": 0, "samples": 0, "kinds": {}}


def _mark(scores: dict[str, dict[str, Any]], name: str, kind: Optional[str]) -> None:
    row = scores.setdefault(name, _blank_score())
    row["samples"] = int(row["samples"]) + 1
    if not kind:
        return
    row["errors"] = int(row["errors"]) + 1
    kinds = row.setdefault("kinds", {})
    kinds[kind] = int(kinds.get(kind) or 0) + 1


def _agent_key(item: dict[str, Any]) -> str:
    raw = str(item.get("name") or item.get("agent_name") or "")
    return _AGENT_ALIASES.get(raw, raw)


def _agent_dir(item: dict[str, Any]) -> str:
    vote = str(item.get("vote") or "").upper()
    if vote in {"BUY", "BULLISH", "LONG"}:
        return "bullish"
    if vote in {"SELL", "BEARISH", "SHORT"}:
        return "bearish"
    if vote == "WAIT":
        return "neutral"
    return str(item.get("direction") or "neutral")


def classify_agents(session: Session, user: User) -> dict[str, Any]:
    """Score hunter + analysis + execution errors from closed bot fills."""
    rows = _closed_rows(session, user)
    bot_rows = [row for row in rows if (row.source or "") == "execution_bot"]
    scores = {name: _blank_score() for name in AGENT_KEYS}
    events: list[dict[str, Any]] = []
    for row in bot_rows:
        outcome = _outcome(row)
        if outcome == "flat":
            continue
        review = swarm.find(session, row.signal_key or "")
        wanted = (review.side if review else ("bearish" if row.side == "short" else "bullish")).strip().lower()
        opposite = "bearish" if wanted == "bullish" else "bullish"
        agents = swarm.agents_of(review) if review else []
        if outcome == "loss":
            _mark(scores, "hunter", "hunter_false_signal")
            _mark(scores, "execution", "execution_losing_fill")
            blamed = ["hunter", "execution"]
            for item in agents:
                name = _agent_key(item)
                if name not in scores:
                    continue
                direction = _agent_dir(item)
                if direction == wanted:
                    _mark(scores, name, "false_confirm")
                    blamed.append(name)
                else:
                    _mark(scores, name, None)
        else:
            _mark(scores, "hunter", None)
            _mark(scores, "execution", None)
            blamed = []
            for item in agents:
                name = _agent_key(item)
                if name not in scores:
                    continue
                direction = _agent_dir(item)
                if direction == opposite:
                    _mark(scores, name, "wrong_direction")
                    blamed.append(name)
                else:
                    _mark(scores, name, None)
        events.append(
            {
                "symbol": row.symbol,
                "timeframe": row.timeframe,
                "outcome": outcome,
                "pnl": float(row.pnl or 0),
                "status": review.status if review else "unreviewed",
                "votes_for": int(review.votes_for) if review else 0,
                "blamed": blamed,
            }
        )
    ranked = sorted(scores.items(), key=lambda item: (item[1]["errors"], item[1]["samples"]), reverse=True)
    return {
        "ok": True,
        "reviewed": len(bot_rows),
        "agents": scores,
        "ranked": [{"name": name, **payload} for name, payload in ranked],
        "events": events[:16],
    }


def _history_check(symbols: list[str]) -> dict[str, Any]:
    reports = []
    for symbol in symbols[:2]:
        try:
            reports.append(backtest(symbol, "1h", horizon=24, reward_multiple=2.0))
        except Exception as exc:  # noqa: BLE001
            reports.append({"symbol": symbol, "error": str(exc)})
    usable = [row for row in reports if "win_rate" in row]
    hist_rate = None
    if usable:
        hist_rate = round(sum(float(row.get("win_rate") or 0) for row in usable) / len(usable), 1)
    return {"samples": reports, "win_rate": hist_rate}


def review(session: Session, user: User, apply_corrections: bool = True) -> dict[str, Any]:
    desk = agent_desk.get_desk(session, user)
    rows = _closed_rows(session, user)
    bot_rows = [row for row in rows if (row.source or "") in REVIEW_SOURCES]
    sample = bot_rows or rows
    wins = [row for row in sample if _outcome(row) == "win"]
    losses = [row for row in sample if _outcome(row) == "loss"]
    flats = [row for row in sample if _outcome(row) == "flat"]
    closed_n = len(wins) + len(losses)
    win_rate = round(len(wins) / closed_n * 100, 1) if closed_n else None
    avg_pnl = round(sum(float(row.pnl or 0) for row in sample) / len(sample), 4) if sample else 0.0
    sl_rate = round(len([row for row in sample if row.reason == "sl"]) / len(sample) * 100, 1) if sample else None
    tp_rate = round(len([row for row in sample if row.reason == "tp"]) / len(sample) * 100, 1) if sample else None
    symbols = []
    seen: set[str] = set()
    for row in sample:
        if row.symbol in seen:
            continue
        seen.add(row.symbol)
        symbols.append(row.symbol)
    history = _history_check(symbols) if symbols else {"samples": [], "win_rate": None}

    before = float(desk.min_confidence)
    after = before
    notes: list[str] = []
    if closed_n >= 6 and win_rate is not None:
        if win_rate < 45:
            after = min(96.0, before + 3.0)
            notes.append("win_rate_low_raise_threshold")
        elif win_rate > 62 and before > 78:
            after = max(78.0, before - 2.0)
            notes.append("win_rate_high_relax_threshold")
        if sl_rate is not None and sl_rate >= 55:
            after = min(96.0, after + 1.5)
            notes.append("stop_rate_high")
    if history.get("win_rate") is not None and win_rate is not None and closed_n >= 4:
        gap = win_rate - float(history["win_rate"])
        if gap <= -12:
            after = min(96.0, after + 2.0)
            notes.append("lagging_historical_win_rate")
        elif gap >= 12:
            notes.append("leading_historical_win_rate")

    applied = False
    if apply_corrections and after != before:
        after = agent_desk.apply_threshold(session, desk, after)
        applied = True
    else:
        after = round(max(75.0, min(96.0, after)), 1)

    params = agent_desk.params_of(desk)
    params.update(
        {
            "win_rate": win_rate,
            "avg_pnl": avg_pnl,
            "sl_rate": sl_rate,
            "tp_rate": tp_rate,
            "historical_win_rate": history.get("win_rate"),
            "min_confidence_before": before,
            "min_confidence_after": after,
            "notes": notes,
            "reviewed_at": _now().isoformat(),
            "sample": closed_n,
        }
    )
    desk.params_json = json.dumps(params, ensure_ascii=False)
    desk.last_audit_at = _now()
    desk.updated_at = _now()
    session.add(desk)
    session.commit()

    payload = {
        "agent": "auditor",
        "kind": "review",
        "reviewed": len(sample),
        "bot_trades": len(bot_rows),
        "wins": len(wins),
        "losses": len(losses),
        "flats": len(flats),
        "win_rate": win_rate,
        "accuracy": win_rate,
        "avg_pnl": avg_pnl,
        "sl_rate": sl_rate,
        "tp_rate": tp_rate,
        "historical": history,
        "swarm": _swarm(session, user, desk, bot_rows),
        "agent_errors": classify_agents(session, user),
        "correction": {"from": before, "to": after, "applied": applied, "notes": notes},
        "book": {
            "cash": paper.get_account(session, user).cash,
            "equity": paper.book(session, user).get("equity"),
            "realized_pnl": paper.book(session, user).get("realized_pnl"),
        },
    }
    agent_desk.write_report(session, user, "audit", "supervisor_review", payload)
    return {"ok": True, "desk": agent_desk.serialize_desk(desk), "audit": payload}


def review_all() -> dict[str, Any]:
    ran = 0
    with Session(engine) as session:
        users = session.exec(select(User).where(User.is_active == True)).all()  # noqa: E712
        for user in users:
            has_work = session.exec(
                select(PaperPosition).where(PaperPosition.user_id == user.id)
            ).first() or session.exec(select(AgentReport).where(AgentReport.user_id == user.id)).first()
            if not has_work:
                continue
            try:
                review(session, user, apply_corrections=True)
                ran += 1
            except Exception:
                continue
    return {"reviewed": ran}
