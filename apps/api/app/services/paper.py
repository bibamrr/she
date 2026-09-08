"""Simulated paper book: reserve cash, mark to last, close on SL/TP."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from sqlmodel import Session, select

from apps.api.app.models import PaperAccount, PaperPosition, User

DEFAULT_CASH = 100000.0
BOT_SOURCE = "execution_bot"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def is_bot(source: str) -> bool:
    return (source or "") == BOT_SOURCE


def _aware(value: Optional[datetime]) -> Optional[datetime]:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def bot_session_start(session: Session) -> datetime:
    from apps.api.app.models import BotDay

    last = session.exec(select(BotDay).order_by(BotDay.id.desc())).first()
    if last and last.reset_at:
        return _aware(last.reset_at) or datetime(1970, 1, 1, tzinfo=timezone.utc)
    return datetime(1970, 1, 1, tzinfo=timezone.utc)


def _in_book(row: PaperPosition, scope: str, since: Optional[datetime]) -> bool:
    bot = is_bot(getattr(row, "source", "") or "")
    if scope == "bot":
        if not bot:
            return False
        if since is None:
            return True
        opened = _aware(row.opened_at)
        return opened is None or opened >= since
    if scope == "manual":
        return not bot
    return True


def normalize_side(side: str) -> str:
    raw = (side or "long").strip().lower()
    if raw in {"short", "bearish", "sell"}:
        return "short"
    return "long"


def unrealized(side: str, entry: float, qty: float, last: float) -> float:
    if side == "short":
        return (entry - last) * qty
    return (last - entry) * qty


def hit_levels(side: str, last: float, stop: float, target: float) -> Optional[str]:
    if side == "short":
        if stop and last >= stop:
            return "sl"
        if target and last <= target:
            return "tp"
        return None
    if stop and last <= stop:
        return "sl"
    if target and last >= target:
        return "tp"
    return None


def _align_bank(account: PaperAccount) -> bool:
    """Keep the virtual book anchored at exactly $100,000 starting capital."""
    start = float(account.starting_cash or 0)
    if abs(start - DEFAULT_CASH) <= 0.5:
        account.starting_cash = DEFAULT_CASH
        return False
    account.cash = round(float(account.cash or 0) + (DEFAULT_CASH - start), 6)
    account.starting_cash = DEFAULT_CASH
    account.updated_at = _now()
    return True


def get_account(session: Session, user: User, seed_cash: Optional[float] = None) -> PaperAccount:
    account = session.exec(select(PaperAccount).where(PaperAccount.user_id == user.id)).first()
    if account:
        if _align_bank(account):
            session.add(account)
            session.commit()
            session.refresh(account)
        return account
    account = PaperAccount(user_id=user.id, cash=DEFAULT_CASH, starting_cash=DEFAULT_CASH, updated_at=_now())
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


def _serialize_position(pos: PaperPosition, last: Optional[float] = None) -> dict[str, Any]:
    mark = float(last) if last is not None else (float(pos.exit) if pos.exit is not None else float(pos.entry))
    live = float(pos.pnl) if pos.status != "open" else unrealized(pos.side, pos.entry, pos.qty, mark)
    return {
        "id": pos.id,
        "symbol": pos.symbol,
        "side": pos.side,
        "qty": pos.qty,
        "entry": pos.entry,
        "stop": pos.stop,
        "target": pos.target,
        "status": pos.status,
        "exit": pos.exit,
        "pnl": round(live, 6),
        "reason": pos.reason,
        "source": getattr(pos, "source", "") or "manual",
        "confidence": float(getattr(pos, "confidence", 0) or 0),
        "timeframe": getattr(pos, "timeframe", "") or "",
        "venue": getattr(pos, "venue", "") or "",
        "signal_key": getattr(pos, "signal_key", "") or "",
        "opened_at": pos.opened_at.isoformat() if pos.opened_at else None,
        "closed_at": pos.closed_at.isoformat() if pos.closed_at else None,
    }


def _positions(session: Session, user: User, scope: str) -> list[PaperPosition]:
    rows = session.exec(
        select(PaperPosition).where(PaperPosition.user_id == user.id).order_by(PaperPosition.id.desc())
    ).all()
    since = bot_session_start(session) if scope == "bot" else None
    return [row for row in rows if _in_book(row, scope, since)]


def ledger(
    session: Session,
    user: User,
    scope: str = "manual",
    last_by_symbol: Optional[dict[str, float]] = None,
) -> dict[str, Any]:
    rows = _positions(session, user, scope)
    open_rows = [row for row in rows if row.status == "open"]
    closed_rows = [row for row in rows if row.status != "open"]
    marks = last_by_symbol or {}
    realized = sum(float(row.pnl or 0) for row in closed_rows)
    reserved = 0.0
    floating = 0.0
    open_payload = []
    for row in open_rows:
        last = marks.get(row.symbol)
        item = _serialize_position(row, last)
        open_payload.append(item)
        reserved += float(row.qty) * float(row.entry)
        if last is not None:
            floating += float(item["pnl"])
    cash = DEFAULT_CASH + realized - reserved
    equity = DEFAULT_CASH + realized + floating
    return {
        "cash": round(max(0.0, cash), 6),
        "starting_cash": DEFAULT_CASH,
        "equity": round(equity, 6),
        "realized_pnl": round(realized, 6),
        "unrealized_pnl": round(floating, 6),
        "open": open_payload,
        "closed": [_serialize_position(row) for row in closed_rows[:40]],
        "scope": scope,
    }


def available_cash(session: Session, user: User, scope: str = "manual") -> float:
    return float(ledger(session, user, scope)["cash"])


def book(
    session: Session,
    user: User,
    last_by_symbol: Optional[dict[str, float]] = None,
    scope: str = "manual",
) -> dict[str, Any]:
    data = ledger(session, user, scope, last_by_symbol)
    if scope == "manual":
        account = get_account(session, user)
        if abs(float(account.cash or 0) - float(data["cash"])) > 0.05:
            account.cash = float(data["cash"])
            account.starting_cash = DEFAULT_CASH
            account.updated_at = _now()
            session.add(account)
    return data


def open_trade(
    session: Session,
    user: User,
    symbol: str,
    side: str,
    qty: float,
    entry: float,
    stop: float,
    target: float,
    seed_cash: Optional[float] = None,
    source: str = "manual",
    confidence: float = 0.0,
    timeframe: str = "",
    venue: str = "",
    signal_key: str = "",
) -> dict[str, Any]:
    symbol = symbol.strip().upper()
    side = normalize_side(side)
    qty = float(qty)
    entry = float(entry)
    stop = float(stop or 0)
    target = float(target or 0)
    if not symbol or qty <= 0 or entry <= 0:
        raise ValueError("invalid paper order")
    account = get_account(session, user, seed_cash)
    scope = "bot" if is_bot(source) else "manual"
    notional = qty * entry
    cash = available_cash(session, user, scope)
    if cash + 1e-9 < notional:
        raise ValueError("insufficient paper cash")
    if scope == "manual":
        account.cash = round(cash - notional, 6)
        account.updated_at = _now()
        session.add(account)
    pos = PaperPosition(
        user_id=user.id,
        symbol=symbol,
        side=side,
        qty=qty,
        entry=entry,
        stop=stop,
        target=target,
        status="open",
        source=source or "manual",
        confidence=float(confidence or 0),
        timeframe=timeframe or "",
        venue=venue or "",
        signal_key=signal_key or "",
    )
    session.add(pos)
    session.commit()
    session.refresh(pos)
    return {"ok": True, "position": _serialize_position(pos), **book(session, user, scope="manual")}


def _close_row(account: PaperAccount, pos: PaperPosition, exit_px: float, reason: str) -> None:
    exit_px = float(exit_px)
    pnl = unrealized(pos.side, pos.entry, pos.qty, exit_px)
    if not is_bot(getattr(pos, "source", "") or ""):
        account.cash = round(account.cash + (pos.qty * pos.entry) + pnl, 6)
        account.updated_at = _now()
    pos.status = "closed"
    pos.exit = exit_px
    pos.pnl = round(pnl, 6)
    pos.reason = reason
    pos.closed_at = _now()


def close_trade(session: Session, user: User, position_id: int, exit_px: Optional[float] = None) -> dict[str, Any]:
    account = get_account(session, user)
    pos = session.get(PaperPosition, position_id)
    if not pos or pos.user_id != user.id:
        raise ValueError("position not found")
    if is_bot(getattr(pos, "source", "") or ""):
        raise ValueError("bot fills are admin-only")
    if pos.status != "open":
        return {"ok": True, "position": _serialize_position(pos), **book(session, user, scope="manual")}
    price = float(exit_px) if exit_px and exit_px > 0 else pos.entry
    _close_row(account, pos, price, "manual")
    session.add(account)
    session.add(pos)
    session.commit()
    return {"ok": True, "position": _serialize_position(pos), **book(session, user, scope="manual")}


def mark_symbol(
    session: Session,
    user: User,
    symbol: str,
    last: float,
    scope: str = "all",
) -> dict[str, Any]:
    last = float(last)
    if last <= 0:
        raise ValueError("invalid last price")
    account = get_account(session, user)
    rows = session.exec(
        select(PaperPosition).where(
            PaperPosition.user_id == user.id,
            PaperPosition.symbol == symbol.strip().upper(),
            PaperPosition.status == "open",
        )
    ).all()
    since = bot_session_start(session) if scope == "bot" else None
    closed = 0
    for pos in rows:
        if scope != "all" and not _in_book(pos, scope, since):
            continue
        reason = hit_levels(pos.side, last, pos.stop, pos.target)
        if not reason:
            continue
        _close_row(account, pos, last, reason)
        session.add(pos)
        closed += 1
    if closed:
        session.add(account)
        session.commit()
    view = "manual" if scope == "manual" else "bot" if scope == "bot" else "manual"
    return {"ok": True, "closed": closed, **book(session, user, {symbol.strip().upper(): last}, scope=view)}


def flatten_bot(session: Session, user: User, last_by_symbol: Optional[dict[str, float]] = None) -> int:
    """Close open execution-bot fills so the daily bank can reset cleanly."""
    account = get_account(session, user)
    rows = session.exec(
        select(PaperPosition).where(
            PaperPosition.user_id == user.id,
            PaperPosition.status == "open",
            PaperPosition.source == "execution_bot",
        )
    ).all()
    marks = last_by_symbol or {}
    closed = 0
    for pos in rows:
        last = float(marks.get(pos.symbol) or 0)
        exit_px = last if last > 0 else float(pos.entry)
        _close_row(account, pos, exit_px, "daily_reset")
        session.add(pos)
        closed += 1
    if closed:
        session.add(account)
        session.commit()
    return closed


def restore_bank(session: Session, user: User) -> None:
    """Put the virtual bank back to $100,000, keeping leftover manual reserved cash."""
    account = get_account(session, user)
    manual = session.exec(
        select(PaperPosition).where(
            PaperPosition.user_id == user.id,
            PaperPosition.status == "open",
        )
    ).all()
    reserved = sum(float(row.qty) * float(row.entry) for row in manual if (row.source or "") != "execution_bot")
    account.cash = round(max(0.0, DEFAULT_CASH - reserved), 6)
    account.starting_cash = DEFAULT_CASH
    account.updated_at = _now()
    session.add(account)
    session.commit()


def reset_book(session: Session, user: User, cash: Optional[float] = None) -> dict[str, Any]:
    _ = cash
    account = get_account(session, user)
    rows = session.exec(select(PaperPosition).where(PaperPosition.user_id == user.id)).all()
    for row in rows:
        if is_bot(getattr(row, "source", "") or ""):
            continue
        session.delete(row)
    account.cash = DEFAULT_CASH
    account.starting_cash = DEFAULT_CASH
    account.updated_at = _now()
    session.add(account)
    session.commit()
    return book(session, user, scope="manual")
