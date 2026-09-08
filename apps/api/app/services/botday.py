"""Daily bot session: snapshot at 12:00 Arabia, then restore the $100,000 bank."""

from __future__ import annotations

import threading
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from sqlmodel import Session, select

from apps.api.app.db import engine
from apps.api.app.models import BotDay, PaperPosition, User
from apps.api.app.services import paper
from apps.api.app.services.market import fetch_ticker

RIYADH = timezone(timedelta(hours=3))
RESET_HOUR = 12
_LOCK = threading.Lock()
_MARK_CACHE: tuple[float, dict[str, float]] = (0.0, {})


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _local_now() -> datetime:
    return datetime.now(RIYADH)


def _iso(value: Optional[datetime]) -> Optional[str]:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.isoformat()


def next_reset_at(now: Optional[datetime] = None) -> datetime:
    local = now or _local_now()
    target = local.replace(hour=RESET_HOUR, minute=0, second=0, microsecond=0)
    if local >= target:
        target = target + timedelta(days=1)
    return target.astimezone(timezone.utc)


def last_day(session: Session) -> Optional[BotDay]:
    return session.exec(select(BotDay).order_by(BotDay.id.desc())).first()


def _cached_marks(symbols: list[str]) -> dict[str, float]:
    global _MARK_CACHE
    wanted = [item for item in symbols if item]
    if not wanted:
        return {}
    stamp, cache = _MARK_CACHE
    if time.time() - stamp < 45 and all(item in cache for item in wanted):
        return cache
    marks = dict(cache)
    marks.update(_mark_map(wanted))
    _MARK_CACHE = (time.time(), marks)
    return marks


def session_stats(session: Session, last_by_symbol: Optional[dict[str, float]] = None) -> dict[str, Any]:
    since = paper.bot_session_start(session)
    rows = session.exec(select(PaperPosition).where(PaperPosition.source == paper.BOT_SOURCE)).all()
    live = [row for row in rows if paper._in_book(row, "bot", since)]
    opened = live
    closed = [row for row in live if row.status != "open"]
    opens = [row for row in live if row.status == "open"]
    wins = [row for row in closed if row.reason == "tp" or float(row.pnl or 0) > 0]
    losses = [row for row in closed if row.reason == "sl" or float(row.pnl or 0) < 0]
    profit = round(sum(float(row.pnl or 0) for row in wins), 4)
    loss = round(abs(sum(float(row.pnl or 0) for row in losses)), 4)
    realized = round(sum(float(row.pnl or 0) for row in closed), 4)
    marks = last_by_symbol if last_by_symbol is not None else _cached_marks(list({row.symbol for row in opens}))
    floating = 0.0
    for row in opens:
        last = marks.get(row.symbol)
        if last is None:
            continue
        floating += paper.unrealized(row.side, row.entry, row.qty, float(last))
    by_user: dict[int, list[Any]] = defaultdict(list)
    for row in live:
        by_user[int(row.user_id or 0)].append(row)
    equities = []
    for pack in by_user.values():
        closed_pnl = sum(float(row.pnl or 0) for row in pack if row.status != "open")
        open_pnl = 0.0
        for row in pack:
            if row.status != "open":
                continue
            last = marks.get(row.symbol)
            if last is None:
                continue
            open_pnl += paper.unrealized(row.side, row.entry, row.qty, float(last))
        equities.append(paper.DEFAULT_CASH + closed_pnl + open_pnl)
    wallet = round(sum(equities) / len(equities), 2) if equities else paper.DEFAULT_CASH
    return {
        "opened": len(opened),
        "open_now": len(opens),
        "closed": len(closed),
        "wins": len(wins),
        "losses": len(losses),
        "profit": profit,
        "loss": loss,
        "realized_pnl": realized,
        "unrealized_pnl": round(floating, 4),
        "wallet": wallet,
        "starting_cash": paper.DEFAULT_CASH,
        "session_started_at": _iso(since) if since.year > 1970 else None,
    }


def _mark_map(symbols: list[str]) -> dict[str, float]:
    marks: dict[str, float] = {}
    for symbol in symbols:
        try:
            ticker = fetch_ticker(symbol)
            last = float(ticker.get("last") or 0)
            if last > 0:
                marks[symbol] = last
        except Exception:
            continue
    return marks


def roll_day(session: Session, day: str) -> dict[str, Any]:
    opens = session.exec(
        select(PaperPosition).where(PaperPosition.source == paper.BOT_SOURCE, PaperPosition.status == "open")
    ).all()
    marks = _mark_map(list({row.symbol for row in opens}))
    snap = session_stats(session, marks)
    users = {int(row.user_id) for row in opens}
    for user_id in users:
        user = session.get(User, user_id)
        if not user:
            continue
        paper.flatten_bot(session, user, marks)
    row = BotDay(
        day=day,
        opened=int(snap["opened"]),
        wins=int(snap["wins"]),
        losses=int(snap["losses"]),
        profit=float(snap["profit"]),
        loss=float(snap["loss"]),
        realized_pnl=float(snap["realized_pnl"]),
        unrealized_pnl=float(snap["unrealized_pnl"]),
        wallet=float(snap["wallet"]),
        reset_at=_now(),
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return {"ok": True, "day": day, "reset_at": _iso(row.reset_at), **snap}


def maybe_roll() -> Optional[dict[str, Any]]:
    local = _local_now()
    today = local.date().isoformat()
    if local.hour < RESET_HOUR:
        return None
    with _LOCK:
        with Session(engine) as session:
            last = last_day(session)
            if last and last.day == today:
                return None
            try:
                return roll_day(session, today)
            except Exception:
                session.rollback()
                raise


def report(session: Session) -> dict[str, Any]:
    live = session_stats(session)
    last = last_day(session)
    history = session.exec(select(BotDay).order_by(BotDay.id.desc())).all()[:14]
    return {
        "live": live,
        "last_reset_at": _iso(last.reset_at) if last else None,
        "last_day": last.day if last else None,
        "next_reset_at": _iso(next_reset_at()),
        "reset_hour": RESET_HOUR,
        "timezone": "Asia/Riyadh",
        "history": [
            {
                "day": row.day,
                "opened": row.opened,
                "wins": row.wins,
                "losses": row.losses,
                "profit": row.profit,
                "loss": row.loss,
                "realized_pnl": row.realized_pnl,
                "wallet": row.wallet,
                "reset_at": _iso(row.reset_at),
            }
            for row in history
        ],
    }
