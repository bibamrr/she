from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from apps.api.app.models import User
from apps.api.app.security import get_optional_user
from apps.api.app.services import access
from apps.api.app.services.market import (
    TIMEFRAMES,
    fetch_ohlcv,
    is_crypto,
    normalize_timeframe,
    rows_to_candles,
)
from engine.indicator_pack import CATALOG, compute_pack
from engine.shc_orchestrator import ohlcv_to_df

router = APIRouter(prefix="/api/indicators", tags=["indicators"])


@router.get("/catalog")
def catalog(user: Optional[User] = Depends(get_optional_user)) -> dict:
    full_vrcs = access.has_feature(user, "vrcs")
    items = []
    for item in CATALOG:
        row = dict(item)
        locked = item["id"] == access.VRCS_ID and not full_vrcs
        row["locked"] = locked
        row["min_tier"] = "pro_hunter" if item["id"] == access.VRCS_ID else "explorer"
        items.append(row)
    return {"indicators": items, "timeframes": TIMEFRAMES, "classic": sorted(access.CLASSIC_INDICATORS)}


@router.get("/compute")
def compute(
    symbol: str = Query(default="BTC/USDT"),
    timeframe: str = Query(default="15m"),
    ids: str = Query(default="vrcs,volume,ema12"),
    limit: int = Query(default=400, ge=80, le=1500),
    compression_period: int = Query(default=20, ge=5, le=200),
    threshold_multiplier: float = Query(default=0.6, ge=0.1, le=1.5),
    volume_factor: float = Query(default=0.7, ge=0.1, le=1.5),
    lookback_breakout: int = Query(default=3, ge=1, le=20),
    user: Optional[User] = Depends(get_optional_user),
) -> dict[str, Any]:
    if not is_crypto(symbol) and not access.has_feature(user, "live_equities"):
        if not access.has_feature(user, "delayed_equities"):
            raise HTTPException(status_code=403, detail={"code": "upgrade_required", "feature": "live_equities"})
        delayed = True
    else:
        delayed = False
    source_tf = normalize_timeframe(timeframe)
    try:
        rows = fetch_ohlcv(symbol, source_tf, limit, delayed=delayed)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    candles = rows_to_candles(rows)
    df = ohlcv_to_df(rows)
    df["time"] = [c["time"] for c in candles]
    wanted = access.allowed_indicators(user, [item.strip() for item in ids.split(",") if item.strip()])
    pack = compute_pack(
        df,
        wanted,
        {
            "compression_period": compression_period,
            "threshold_multiplier": threshold_multiplier,
            "volume_factor": volume_factor,
            "lookback_breakout": lookback_breakout,
        },
    )
    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "source_timeframe": source_tf,
        "candles": candles,
        "delayed": delayed,
        "allowed_ids": wanted,
        **pack,
    }
