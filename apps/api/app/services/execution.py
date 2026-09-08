"""Execution worker: confirmed Hunter hits only → virtual book. Never invents setups."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from sqlmodel import Session, select

from apps.api.app.db import engine
from apps.api.app.models import AgentDesk, PaperPosition, User
from apps.api.app.services import desk as agent_desk
from apps.api.app.services import paper
from apps.api.app.services import swarm
from apps.api.app.services.hunter import hunt, is_followable, is_launchable, match_official
from apps.api.app.services.market import fetch_ticker
from apps.api.app.services.stables import is_stablecoin

DESKS = agent_desk.DESKS
EXEC_TIMEFRAMES = ("1m", "5m", "15m", "30m", "1h", "4h", "1d")
EQUITY_TIMEFRAMES = ("5m", "15m", "30m", "1h", "4h", "1d")
FOLLOW_FLOOR = 60.0
# A full sweep of every timeframe costs more than one loop interval (equity
# candles are serialised behind the TradingView socket), so each cycle walks a
# slice of the frames and the rotation covers them all over a few minutes.
CRYPTO_FRAMES_PER_CYCLE = 4
EQUITY_FRAMES_PER_CYCLE = 2
_ROTATE = 0
_FRAME_ROTATE = 0
_TF_WEIGHT = {
    "1m": 0.55,
    "5m": 0.7,
    "15m": 0.9,
    "30m": 1.0,
    "1h": 1.15,
    "4h": 1.3,
    "1d": 1.5,
}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def get_desk(session: Session, user: User) -> AgentDesk:
    return agent_desk.get_desk(session, user)


def serialize_desk(desk: AgentDesk) -> dict[str, Any]:
    return agent_desk.serialize_desk(desk)


def save_desk(
    session: Session,
    user: User,
    enabled: Optional[bool] = None,
    venue: Optional[str] = None,
    min_confidence: Optional[float] = None,
    max_open: Optional[int] = None,
    risk_pct: Optional[float] = None,
) -> AgentDesk:
    # min_confidence is ignored: the auditor is the only writer of the threshold.
    _ = enabled, min_confidence
    # risk_pct is ignored: the bot sizes fills on its own for the auditor.
    _ = risk_pct
    return agent_desk.save_runtime(session, user, venue=venue, max_open=max_open)


def write_report(session: Session, user: User, kind: str, title: str, body: dict[str, Any]):
    return agent_desk.write_report(session, user, kind, title, body)


def list_reports(session: Session, user: User, kind: str = "", limit: int = 20) -> list[dict[str, Any]]:
    return agent_desk.list_reports(session, user, kind, limit)


def signal_key(hit: dict[str, Any]) -> str:
    signal = hit.get("signal") or {}
    return "|".join(
        [
            str(hit.get("symbol") or ""),
            str(hit.get("timeframe") or ""),
            str(signal.get("time") or hit.get("time") or ""),
            str(round(float(hit.get("confidence") or 0), 1)),
        ]
    )


def confirmed(hit: dict[str, Any], min_confidence: float) -> bool:
    return is_launchable(hit, min_confidence)


def _bot_notional(account: Any, confidence: float, timeframe: str, cash: Optional[float] = None) -> float:
    """Autonomous size from the $100k bank. No subscriber amount or risk %."""
    bank = float(account.starting_cash or paper.DEFAULT_CASH)
    conf = max(60.0, min(100.0, float(confidence or 60.0)))
    conf_factor = 0.45 + ((conf - 60.0) / 40.0) * 0.75
    tf = _TF_WEIGHT.get(str(timeframe or "").strip().lower(), 1.0)
    notional = bank * 0.01 * conf_factor * tf
    notional = max(250.0, min(2500.0, notional))
    available = float(bank if cash is None else cash)
    if notional > available:
        notional = max(0.0, available * 0.97)
    return float(notional)


def _qty(
    account: Any,
    entry: float,
    confidence: float = 60.0,
    timeframe: str = "",
    cash: Optional[float] = None,
) -> float:
    if entry <= 0:
        return 0.0
    notional = _bot_notional(account, confidence, timeframe, cash)
    return max(0.0, float(notional / entry))


def mark_open(session: Session, user: User) -> int:
    rows = session.exec(
        select(PaperPosition).where(PaperPosition.user_id == user.id, PaperPosition.status == "open")
    ).all()
    closed = 0
    seen: set[str] = set()
    for row in rows:
        if row.symbol in seen:
            continue
        seen.add(row.symbol)
        try:
            ticker = fetch_ticker(row.symbol)
            last = float(ticker.get("last") or 0)
            if last <= 0:
                continue
            result = paper.mark_symbol(session, user, row.symbol, last)
            closed += int(result.get("closed") or 0)
        except Exception:
            continue
    return closed


def execute_hit(
    session: Session,
    user: User,
    hit: dict[str, Any],
    desk: Optional[AgentDesk] = None,
    trust_hunter: bool = False,
) -> dict[str, Any]:
    desk = desk or get_desk(session, user)
    floor = float(desk.min_confidence)
    if trust_hunter and is_followable(hit, FOLLOW_FLOOR) and hit.get("source") == "hunter":
        official = hit
    else:
        official = match_official(hit, min(FOLLOW_FLOOR, floor))
    if not official:
        return {"ok": False, "skipped": "not_hunter"}
    symbol = str(official.get("symbol") or "").strip().upper()
    if is_stablecoin(symbol):
        return {"ok": False, "skipped": "stablecoin"}
    key = str(official.get("signal_key") or signal_key(official))
    if not swarm.is_approved(session, key):
        return {"ok": False, "skipped": "not_swarm_approved"}
    since = paper.bot_session_start(session)
    bot_rows = session.exec(
        select(PaperPosition).where(
            PaperPosition.user_id == user.id,
            PaperPosition.source == paper.BOT_SOURCE,
        )
    ).all()
    session_bot = [row for row in bot_rows if paper._in_book(row, "bot", since)]
    if key:
        seen = next((row for row in session_bot if (row.signal_key or "") == key), None)
        if seen:
            return {"ok": False, "skipped": "duplicate", "position": paper._serialize_position(seen)}
    bot_open = [row for row in session_bot if row.status == "open"]
    if any(row.symbol == symbol for row in bot_open):
        return {"ok": False, "skipped": "already_open", "symbol": symbol}
    cap = max(int(desk.max_open), 12)
    if len(bot_open) >= cap:
        return {"ok": False, "skipped": "max_open"}
    entry = float(official.get("entry") or 0)
    stop = float(official.get("stop") or 0)
    target = float(official.get("target") or 0)
    if entry <= 0 or stop <= 0 or target <= 0:
        return {"ok": False, "skipped": "incomplete_hunter_setup"}
    side = "short" if official.get("side") == "bearish" else "long"
    account = paper.get_account(session, user)
    bot_cash = paper.available_cash(session, user, "bot")
    confidence = float(official.get("confidence") or 0)
    timeframe = str(official.get("timeframe") or "")
    qty = _qty(account, entry, confidence, timeframe, cash=bot_cash)
    if qty <= 0:
        return {"ok": False, "skipped": "no_size"}
    try:
        result = paper.open_trade(
            session,
            user,
            symbol,
            side,
            qty,
            entry,
            stop,
            target,
            paper.DEFAULT_CASH,
            source="execution_bot",
            confidence=confidence,
            timeframe=timeframe,
            venue=str(official.get("venue") or ""),
            signal_key=key,
        )
    except ValueError as exc:
        return {"ok": False, "skipped": str(exc)}
    report = {
        "agent": "execution_bot",
        "source": "swarm",
        "signal_key": key,
        "symbol": symbol,
        "side": side,
        "entry": entry,
        "stop": stop,
        "target": target,
        "qty": qty,
        "notional": round(qty * entry, 4),
        "sizing": "autonomous",
        "confidence": confidence,
        "state": official.get("state"),
        "venue": official.get("venue"),
        "timeframe": timeframe,
        "position_id": (result.get("position") or {}).get("id"),
    }
    agent_desk.write_report(session, user, "execution", f"{symbol} {side}", report)
    desk.last_tick_at = _now()
    session.add(desk)
    session.commit()
    from apps.api.app.services import auditor

    auditor.observe_fill(session, user, report)
    return {"ok": True, **result, "report": report}


def execute_hits(
    session: Session,
    user: User,
    hits: list[dict[str, Any]],
    desk: Optional[AgentDesk] = None,
    trust_hunter: bool = False,
) -> dict[str, Any]:
    desk = desk or get_desk(session, user)
    opened: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for hit in hits:
        result = execute_hit(session, user, hit, desk, trust_hunter=trust_hunter)
        if result.get("ok"):
            opened.append(result.get("report") or result.get("position") or {})
        else:
            skipped.append({"symbol": hit.get("symbol"), "reason": result.get("skipped")})
    desk.last_tick_at = _now()
    session.add(desk)
    session.commit()
    return {"opened": opened, "skipped": skipped[:12], "desk": serialize_desk(desk), **paper.book(session, user)}


def _frames_for(venue: str) -> tuple[str, ...]:
    return EXEC_TIMEFRAMES if venue == "crypto" else EQUITY_TIMEFRAMES


def _cycle_frames(venue: str, offset: int) -> tuple[str, ...]:
    """Rotating slice of a desk's timeframes so one cycle stays inside its budget."""
    frames = _frames_for(venue)
    take = CRYPTO_FRAMES_PER_CYCLE if venue == "crypto" else EQUITY_FRAMES_PER_CYCLE
    if take >= len(frames):
        return frames
    start = offset % len(frames)
    doubled = frames + frames
    return tuple(doubled[start : start + take])


def gather_hunter_hits(
    venue: str,
    frames: Optional[tuple[str, ...]] = None,
    background: bool = False,
) -> tuple[list[dict[str, Any]], int]:
    """Pull every live Hunter setup across the given timeframes for a desk."""
    seen: set[str] = set()
    hits: list[dict[str, Any]] = []
    scanned = 0
    top = 12 if venue == "crypto" else 8
    for timeframe in frames if frames is not None else _frames_for(venue):
        data = hunt(timeframe, top, FOLLOW_FLOOR, 1.5, venue=venue, background=background)
        scanned += int(data.get("scanned") or 0)
        for hit in data.get("hits") or []:
            if not is_followable(hit, FOLLOW_FLOOR):
                continue
            key = signal_key(hit)
            if key in seen:
                continue
            seen.add(key)
            packed = dict(hit)
            packed["signal_key"] = key
            hits.append(packed)
    hits.sort(key=lambda row: (float(row.get("confidence") or 0), float(row.get("volume_ratio") or 0)), reverse=True)
    return hits, scanned


def tick(session: Session, user: User, venue: Optional[str] = None, hits: Optional[list[dict[str, Any]]] = None) -> dict[str, Any]:
    # Client-supplied hits are ignored — Hunter is the only opportunity source.
    _ = hits
    desk = get_desk(session, user)
    closed = mark_open(session, user)
    wanted = (venue or "auto").strip().lower()
    if wanted == "auto":
        wanted = DESKS[_ROTATE % len(DESKS)]
    if wanted not in DESKS:
        wanted = "crypto"
    ready, scanned = gather_hunter_hits(wanted, _cycle_frames(wanted, _FRAME_ROTATE))
    swarm.review_hits(session, ready)
    approved = swarm.live_approved(session)
    result = execute_hits(session, user, approved, desk, trust_hunter=True)
    result["closed"] = closed
    result["scanned"] = scanned
    result["venue"] = wanted
    result["timeframes"] = list(_frames_for(wanted))
    result["confirmed"] = len(ready)
    result["approved"] = len(approved)
    result["source"] = "swarm"
    return result


def tick_all() -> dict[str, Any]:
    global _ROTATE, _FRAME_ROTATE
    venue = DESKS[_ROTATE % len(DESKS)]
    _ROTATE += 1
    offset = _FRAME_ROTATE
    _FRAME_ROTATE += 1
    frames = _cycle_frames(venue, offset)
    hits, scanned = gather_hunter_hits(venue, frames, background=True)
    if venue != "crypto":
        # Crypto is cheap and always on; equity desks only get their rotating slice.
        extra, extra_scanned = gather_hunter_hits("crypto", _cycle_frames("crypto", offset), background=True)
        hits.extend(extra)
        scanned += extra_scanned
        hits.sort(key=lambda row: (float(row.get("confidence") or 0), float(row.get("volume_ratio") or 0)), reverse=True)
    users_run = 0
    opened = 0
    approved_n = 0
    with Session(engine) as session:
        swarm.review_hits(session, hits)
        approved = swarm.live_approved(session)
        approved_n = len(approved)
        users = session.exec(select(User).where(User.is_active == True)).all()  # noqa: E712
        for user in users:
            desk = get_desk(session, user)
            desk.execution_enabled = True
            desk.venue = "auto"
            mark_open(session, user)
            result = execute_hits(session, user, approved, desk, trust_hunter=True)
            users_run += 1
            opened += len(result.get("opened") or [])
    return {
        "venue": venue,
        "timeframes": list(frames),
        "scanned": scanned,
        "hits": len(hits),
        "approved": approved_n,
        "users": users_run,
        "opened": opened,
        "source": "swarm",
    }


def status(session: Session, user: User) -> dict[str, Any]:
    row = get_desk(session, user)
    book = paper.book(session, user, scope="manual")
    bot_book = paper.book(session, user, scope="bot")
    bot_open = bot_book.get("open") or []
    bot_closed = bot_book.get("closed") or []
    return {
        "desk": serialize_desk(row),
        "book": book,
        "bot_open": bot_open,
        "bot_closed": bot_closed[:12],
        "reports": list_reports(session, user, "", 8),
    }
