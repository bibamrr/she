from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response

from apps.api.app.models import User
from apps.api.app.security import get_optional_user
from apps.api.app.services import access, insight, logos, overview
from apps.api.app.services.scanner import EQUITY_VENUES, scan_crypto, scan_desk, search_assets

router = APIRouter(prefix="/api/market", tags=["scanner"])


def _delay_scan(data: dict) -> dict:
    for key in ("gainers", "losers", "mcap", "active"):
        rows = list(data.get(key) or [])[:8]
        for row in rows:
            row["delayed"] = True
        data[key] = rows
    data["sectors"] = list(data.get("sectors") or [])[:6]
    data["delayed"] = True
    data["upgrade"] = "pro_hunter"
    return data


@router.get("/scan")
def scan(
    venue: str = Query(default="crypto"),
    user: Optional[User] = Depends(get_optional_user),
) -> dict:
    try:
        desk = "tadawul" if venue in {"ksa", "saudi"} else venue
        if desk in EQUITY_VENUES:
            if not access.has_feature(user, "live_equities"):
                if not access.has_feature(user, "delayed_equities"):
                    raise HTTPException(status_code=403, detail={"code": "upgrade_required", "feature": "live_equities"})
                return _delay_scan(scan_desk(desk))
            return scan_desk(desk)
        return scan_crypto()
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/indices")
def indices() -> dict:
    try:
        return overview.tape()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/fundamentals")
def fundamentals(symbol: str = Query(default="BTC/USDT"), timeframe: str = Query(default="1h")) -> dict:
    try:
        return insight.fundamentals(symbol, timeframe)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/sentiment")
def sentiment(symbol: str = Query(default="BTC/USDT"), timeframe: str = Query(default="1h")) -> dict:
    try:
        return insight.sentiment(symbol, timeframe)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/quotes")
def batch_quotes(symbols: str = Query(default="")) -> dict:
    items = [item.strip() for item in symbols.split(",") if item.strip()]
    try:
        return {"quotes": overview.quotes(items)}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/search")
def search(
    q: str = Query(default="", min_length=1),
    venue: str = Query(default=""),
) -> dict:
    try:
        results = search_assets(q)
        if venue in {"crypto", "tadawul", "us", "europe", "asia", "commodities"}:
            focused = [row for row in results if row.get("venue") == venue]
            results = focused or results
        return {"results": results, "venue": venue or "all"}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/logo")
def asset_logo(symbol: str = Query(..., min_length=1, max_length=32)) -> Response:
    payload = logos.resolve(symbol)
    if not payload:
        raise HTTPException(status_code=404, detail="logo not found")
    body, content_type = payload
    return Response(
        content=body,
        media_type=content_type,
        headers={"Cache-Control": "public, max-age=86400"},
    )
