"""Hunter hits → eight analysis agents. Execution may take coordinator-approved rows only."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from sqlmodel import Session, select

from apps.api.app.models import SwarmReview
from apps.api.app.services.hunter import is_followable
from apps.api.app.services.market import fetch_ohlcv, fetch_order_book, parse_market_symbol
from engine.coordinator import (
    BUY,
    REQUIRED_MAJORITY,
    SELL,
    SUB_AGENTS,
    MasterCoordinator,
    direction_from_vote,
    filter_ui_view,
    results_from_agents,
    vote_from_direction,
)
from engine.shc_orchestrator import run_shc_analysis

LIVE_MINUTES = 180
AGENT_NAMES = tuple(SUB_AGENTS)
COORDINATOR = MasterCoordinator(required_majority=REQUIRED_MAJORITY)
_TF_SECONDS = {
    "1s": 1,
    "1m": 60,
    "3m": 180,
    "5m": 300,
    "15m": 900,
    "30m": 1800,
    "1h": 3600,
    "2h": 7200,
    "4h": 14400,
    "6h": 21600,
    "12h": 43200,
    "1d": 86400,
    "3d": 259200,
    "1w": 604800,
    "1M": 2592000,
}
_TF_BARS = {
    "1s": 30,
    "1m": 8,
    "3m": 6,
    "5m": 6,
    "15m": 4,
    "30m": 4,
    "1h": 3,
    "2h": 3,
    "4h": 2,
    "6h": 2,
    "12h": 2,
    "1d": 2,
    "3d": 1,
    "1w": 1,
    "1M": 1,
}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def hunter_side(hit: dict[str, Any]) -> str:
    raw = str(hit.get("side") or "").strip().lower()
    if raw in {"bearish", "short", "sell"}:
        return "bearish"
    return "bullish"


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


def agents_of(row: SwarmReview) -> list[dict[str, Any]]:
    return _parse_agents(row.agents_json)


def _parse_agents(raw: str) -> list[dict[str, Any]]:
    try:
        data = json.loads(raw or "[]")
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _parse_body(raw: str) -> dict[str, Any]:
    try:
        data = json.loads(raw or "{}")
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _iso(value: Optional[datetime]) -> Optional[str]:
    stamp = _as_utc(value)
    return stamp.isoformat() if stamp else None


def market_type_of(symbol: str) -> str:
    spec = parse_market_symbol(symbol)
    if spec.get("crypto") and spec.get("market_type") == "futures":
        return "futures"
    return "spot"


def trade_kind_of(symbol: str, vote: str) -> str:
    market = market_type_of(symbol)
    sell = str(vote or "").upper() == SELL
    if market == "futures":
        return "futuresSell" if sell else "futuresBuy"
    return "spotSell" if sell else "spotBuy"


def entry_window(timeframe: str, start: Optional[datetime]) -> tuple[datetime, datetime]:
    origin = _as_utc(start) or _now()
    bars = int(_TF_BARS.get(timeframe, 4))
    secs = int(_TF_SECONDS.get(timeframe, 900))
    until = origin + timedelta(seconds=max(1, bars) * max(1, secs))
    return origin, until


def expand_targets(
    entry: float,
    stop: float,
    target: float,
    decision: str,
    raw: Optional[list[Any]] = None,
) -> list[float]:
    tps = [float(item) for item in (raw or []) if item not in (None, "")]
    if len(tps) >= 3:
        return [round(tps[0], 8), round(tps[1], 8), round(tps[2], 8)]
    risk = abs(float(entry or 0) - float(stop or 0))
    sell = str(decision or "").upper() == SELL or (target and entry and float(target) < float(entry))
    if sell:
        tp1 = float(entry) - risk if risk else float(target or 0)
        tp2 = float(target or 0) or (float(entry) - risk * 2 if risk else 0.0)
        tp3 = float(entry) - risk * 3 if risk else tp2
    else:
        tp1 = float(entry) + risk if risk else float(target or 0)
        tp2 = float(target or 0) or (float(entry) + risk * 2 if risk else 0.0)
        tp3 = float(entry) + risk * 3 if risk else tp2
    if len(tps) == 1:
        tp1 = tps[0]
    elif len(tps) == 2:
        tp1, tp2 = tps[0], tps[1]
    return [round(float(tp1 or 0), 8), round(float(tp2 or 0), 8), round(float(tp3 or 0), 8)]


def setup_fields(row: SwarmReview, body: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    pack = body if body is not None else _parse_body(row.body_json)
    levels = pack.get("levels") if isinstance(pack.get("levels"), dict) else {}
    vote = str(pack.get("vote") or vote_from_direction(row.direction or row.side))
    targets = expand_targets(
        float(row.entry or 0),
        float(row.stop or 0),
        float(row.target or 0),
        vote,
        levels.get("targets"),
    )
    start, until = entry_window(row.timeframe, row.reviewed_at or row.created_at)
    trade_at = row.reviewed_at or row.created_at
    return {
        "targets": targets,
        "target1": targets[0],
        "target2": targets[1],
        "target3": targets[2],
        "market_type": market_type_of(row.symbol),
        "trade_kind": trade_kind_of(row.symbol, vote),
        "entry_from": _iso(start),
        "entry_until": _iso(until),
        "trade_at": _iso(trade_at),
    }


def serialize(row: SwarmReview) -> dict[str, Any]:
    body = _parse_body(row.body_json)
    vote = str(body.get("vote") or vote_from_direction(row.direction or row.side))
    extra = setup_fields(row, body)
    return {
        "id": row.id,
        "signal_key": row.signal_key,
        "symbol": row.symbol,
        "timeframe": row.timeframe,
        "venue": row.venue,
        "side": row.side,
        "hunter_confidence": float(row.hunter_confidence or 0),
        "entry": float(row.entry or 0),
        "stop": float(row.stop or 0),
        "target": float(extra["target2"] or row.target or 0),
        "status": row.status,
        "votes_for": int(row.votes_for or 0),
        "votes_against": int(row.votes_against or 0),
        "direction": row.direction,
        "vote": vote,
        "success_probability": float(row.success_probability or 0),
        "agents": _parse_agents(row.agents_json),
        "coordinator": body.get("coordinator") or {},
        "created_at": _iso(row.created_at),
        "reviewed_at": _iso(row.reviewed_at),
        **extra,
    }


def to_hit(row: SwarmReview) -> dict[str, Any]:
    extra = setup_fields(row)
    return {
        "symbol": row.symbol,
        "timeframe": row.timeframe,
        "venue": row.venue,
        "side": row.side,
        "vote": vote_from_direction(row.direction or row.side),
        "confidence": float(row.hunter_confidence or 0),
        "entry": float(row.entry or 0),
        "stop": float(row.stop or 0),
        "target": float(extra["target2"] or row.target or 0),
        "source": "hunter",
        "state": "swarm_approved" if row.status == "approved" else row.status,
        "signal": {"time": row.signal_key},
        "signal_key": row.signal_key,
        "swarm_status": row.status,
        **extra,
    }


def find(session: Session, key: str) -> Optional[SwarmReview]:
    if not key:
        return None
    return session.exec(select(SwarmReview).where(SwarmReview.signal_key == key)).first()


def is_approved(session: Session, key: str) -> bool:
    row = find(session, key)
    return bool(row and row.status == "approved")


def _headlines(symbol: str, venue: str) -> list[dict[str, Any]]:
    try:
        from apps.api.app.services.news import fetch_news

        data = fetch_news(venue=venue or "crypto", symbol=symbol, locale="en", limit=8)
        items = data.get("items") if isinstance(data, dict) else None
        return list(items or [])
    except Exception:
        return []


def analysis_package(analysis: dict[str, Any], decision: str, hit: dict[str, Any]) -> dict[str, Any]:
    """Quant/ATR package: entry, stop, and three take-profits for the swarm BUY/SELL."""
    last = float(analysis.get("last_price") or hit.get("entry") or hit.get("last_price") or 0)
    quant = next((item for item in (analysis.get("agents") or []) if item.get("name") == "quant_agent"), {})
    atr = float((quant.get("metrics") or {}).get("atr") or 0)
    quant_vote = str(quant.get("vote") or vote_from_direction(str(quant.get("direction") or "")))
    entry = last
    stop = 0.0
    raw_tps: list[Any] = []
    if quant_vote == decision and quant.get("stop_loss") and quant.get("take_profits"):
        entry = float(quant.get("entry") or last)
        stop = float(quant.get("stop_loss") or 0)
        raw_tps = list(quant.get("take_profits") or [])
    elif last > 0:
        if decision == BUY:
            stop = entry - atr * 1.5 if atr else entry * 0.985
        else:
            stop = entry + atr * 1.5 if atr else entry * 1.015
    if decision == BUY and not (0 < stop < entry):
        stop = entry * 0.985
    if decision == SELL and not (0 < entry < stop):
        stop = entry * 1.015
    target = float(raw_tps[1] if len(raw_tps) > 1 else raw_tps[0] if raw_tps else 0)
    if decision == BUY and not (entry < target if target else False):
        target = entry + atr * 2.0 if atr else entry * 1.03
    if decision == SELL and not (target < entry if target else False):
        target = entry - atr * 2.0 if atr else entry * 0.97
    targets = expand_targets(entry, stop, target, decision, raw_tps)
    return {
        "entry": round(float(entry or 0), 8),
        "stop": round(float(stop or 0), 8),
        "target": targets[1],
        "targets": targets,
    }


def analysis_levels(analysis: dict[str, Any], decision: str, hit: dict[str, Any]) -> tuple[float, float, float]:
    pack = analysis_package(analysis, decision, hit)
    return pack["entry"], pack["stop"], pack["target"]


def _decide(agents: list[dict[str, Any]]) -> dict[str, Any]:
    verdict = COORDINATOR.evaluate_swarm(results_from_agents(agents))
    decision = str(verdict.get("final_decision") or "")
    status = "approved" if verdict.get("status") == "APPROVED" else "rejected"
    if verdict.get("status") == "HOLD":
        status = "hold"
    return {"verdict": verdict, "status": status, "direction": direction_from_vote(decision), "vote": decision}


def review_hit(session: Session, hit: dict[str, Any]) -> SwarmReview:
    key = str(hit.get("signal_key") or signal_key(hit))
    existing = find(session, key)
    if existing and existing.status in {"approved", "rejected", "hold"}:
        return existing
    symbol = str(hit.get("symbol") or "").strip().upper()
    timeframe = str(hit.get("timeframe") or "15m")
    venue = str(hit.get("venue") or "")
    hunter_dir = hunter_side(hit)
    agents: list[dict[str, Any]] = []
    analysis: dict[str, Any] = {}
    direction = "neutral"
    vote = "WAIT"
    probability = 0.0
    verdict: dict[str, Any] = {"status": "HOLD", "reason": "No analysis"}
    status = "hold"
    entry = float(hit.get("entry") or hit.get("last_price") or 0)
    stop = 0.0
    target = 0.0
    targets: list[float] = []
    try:
        ohlcv = fetch_ohlcv(symbol, timeframe, 180)
        book = fetch_order_book(symbol, 50)
        analysis = run_shc_analysis(
            symbol,
            timeframe,
            ohlcv,
            book,
            extras={"news": _headlines(symbol, venue), "hunter": hit, "venue": venue},
        )
        agents = list(analysis.get("agents") or [])
        probability = float(analysis.get("success_probability") or 0)
        decided = _decide(agents)
        verdict = decided["verdict"]
        status = decided["status"]
        direction = decided["direction"]
        vote = str(decided.get("vote") or vote_from_direction(direction))
        if vote in {BUY, SELL}:
            pack = analysis_package(analysis, vote, hit)
            entry, stop, target = pack["entry"], pack["stop"], pack["target"]
            targets = pack["targets"]
    except Exception as exc:  # noqa: BLE001
        agents = [{"name": "swarm", "vote": "WAIT", "direction": "neutral", "confidence": 0, "reasoning": str(exc)}]
        verdict = {"status": "HOLD", "reason": str(exc)}
        status = "hold"
    if status == "approved" and (entry <= 0 or stop <= 0 or target <= 0):
        status = "hold"
        verdict = {**verdict, "status": "HOLD", "reason": "Analysis did not produce a complete IN/SL/TP package."}
    now = _now()
    row = existing or SwarmReview(signal_key=key, created_at=now)
    row.symbol = symbol
    row.timeframe = timeframe
    row.venue = venue
    row.side = direction if direction in {"bullish", "bearish"} else hunter_dir
    row.hunter_confidence = float(hit.get("confidence") or 0)
    row.entry = float(entry or 0)
    row.stop = float(stop or 0)
    row.target = float(target or 0)
    row.status = status
    row.votes_for = int(verdict.get("buy_votes") or 0) if vote == BUY else int(verdict.get("sell_votes") or 0)
    row.votes_against = int(verdict.get("sell_votes") or 0) if vote == BUY else int(verdict.get("buy_votes") or 0)
    row.direction = direction
    row.success_probability = float(verdict.get("average_confidence") or probability or 0)
    row.agents_json = json.dumps(agents, ensure_ascii=False, default=str)
    row.body_json = json.dumps(
        {
            "hunter": hit.get("state"),
            "hunter_side": hunter_dir,
            "vote": vote,
            "levels": {
                "entry": entry,
                "stop": stop,
                "target": target,
                "targets": targets or expand_targets(entry, stop, target, vote),
                "source": "analysis",
            },
            "coordinator": verdict,
        },
        ensure_ascii=False,
        default=str,
    )
    row.reviewed_at = now
    session.add(row)
    session.commit()
    session.refresh(row)
    return row


def review_hits(session: Session, hits: list[dict[str, Any]], limit: int = 8) -> list[SwarmReview]:
    rows: list[SwarmReview] = []
    seen: set[str] = set()
    for hit in hits:
        if not is_followable(hit, 60):
            continue
        key = str(hit.get("signal_key") or signal_key(hit))
        if not key or key in seen:
            continue
        seen.add(key)
        packed = dict(hit)
        packed["signal_key"] = key
        rows.append(review_hit(session, packed))
        if len(rows) >= limit:
            break
    return rows


def _as_utc(value: Optional[datetime]) -> Optional[datetime]:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def live_approved(session: Session) -> list[dict[str, Any]]:
    cutoff = _now() - timedelta(minutes=LIVE_MINUTES)
    rows = [
        row
        for row in session.exec(select(SwarmReview).where(SwarmReview.status == "approved")).all()
        if _as_utc(row.reviewed_at) and _as_utc(row.reviewed_at) >= cutoff
    ]
    rows.sort(key=lambda row: row.id or 0, reverse=True)
    return [to_hit(row) for row in rows]


def board(session: Session, limit: int = 24) -> dict[str, Any]:
    rows = list(session.exec(select(SwarmReview).where(SwarmReview.status == "approved")).all())
    rows.sort(key=lambda row: row.id or 0, reverse=True)
    rows = rows[: max(8, min(int(limit), 40))]
    approved = [serialize(row) for row in rows]
    return {
        "ok": True,
        "required_majority": REQUIRED_MAJORITY,
        "min_confidence": 0.7,
        "agents": list(AGENT_NAMES),
        "approved": approved,
        "waiting": not approved,
        "message": None if approved else "Consensus threshold not met.",
        "ui": [filter_ui_view(row.get("coordinator") or {"status": "APPROVED"}) for row in approved],
    }
