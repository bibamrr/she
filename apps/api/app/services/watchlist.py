from __future__ import annotations

from typing import Any

from sqlmodel import Session, select

from apps.api.app.models import User, WatchItem

MAX_WATCH = 40


def normalize_symbol(raw: str) -> str:
    text = (raw or "").strip()
    if not text:
        return ""
    from apps.api.app.services.market import desk_symbol, is_crypto

    if is_crypto(text) or "/" in text:
        return desk_symbol(text)
    return text.upper()


def list_symbols(session: Session, user: User) -> list[str]:
    rows = session.exec(
        select(WatchItem).where(WatchItem.user_id == user.id).order_by(WatchItem.position, WatchItem.id)
    ).all()
    return [row.symbol for row in rows]


def replace(session: Session, user: User, symbols: list[str]) -> list[str]:
    clean: list[str] = []
    seen: set[str] = set()
    for raw in symbols:
        symbol = normalize_symbol(raw)
        if not symbol or symbol in seen:
            continue
        seen.add(symbol)
        clean.append(symbol)
        if len(clean) >= MAX_WATCH:
            break
    for row in session.exec(select(WatchItem).where(WatchItem.user_id == user.id)).all():
        session.delete(row)
    for index, symbol in enumerate(clean):
        session.add(WatchItem(user_id=user.id or 0, symbol=symbol, position=index))
    session.commit()
    return clean


def add(session: Session, user: User, symbol: str) -> list[str]:
    current = list_symbols(session, user)
    symbol = normalize_symbol(symbol)
    if not symbol:
        raise ValueError("invalid symbol")
    next_list = [symbol, *[item for item in current if item != symbol]]
    return replace(session, user, next_list)


def remove(session: Session, user: User, symbol: str) -> list[str]:
    symbol = normalize_symbol(symbol)
    return replace(session, user, [item for item in list_symbols(session, user) if item != symbol])


def payload(session: Session, user: User) -> dict[str, Any]:
    symbols = list_symbols(session, user)
    return {"symbols": symbols, "count": len(symbols), "max": MAX_WATCH}
