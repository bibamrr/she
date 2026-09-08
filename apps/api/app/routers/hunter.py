from __future__ import annotations

import csv
import io
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse

from apps.api.app.models import User
from apps.api.app.security import get_optional_user
from apps.api.app.services import access
from apps.api.app.services.hunter import (
    backtest,
    correlation_matrix,
    hunt,
    liquid_universe,
    multi_timeframe,
    session_heatmap,
)
from engine.calibration import calibrate, load_profile, save_profile

router = APIRouter(prefix="/api/hunter", tags=["hunter"])


@router.get("/scan")
def scan(
    timeframe: str = Query(default="15m"),
    top: int = Query(default=40, ge=5, le=120),
    min_confidence: float = Query(default=75.0, ge=50.0, le=99.0),
    volume_spike: float = Query(default=2.0, ge=1.0, le=10.0),
    venue: str = Query(default="crypto"),
    user: Optional[User] = Depends(get_optional_user),
) -> dict[str, Any]:
    plan = access.plan_of(user)
    live = access.has_feature(user, "hunter")
    delayed = access.has_feature(user, "hunter_delayed")
    if not live and not delayed:
        raise HTTPException(status_code=403, detail={"code": "upgrade_required", "feature": "hunter"})
    cap = min(top, int(plan["scan_top"]))
    try:
        data = hunt(timeframe, cap, min_confidence, volume_spike, venue=venue)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    if not live:
        delay = int(plan.get("hunter_delay_bars") or 8)
        stale = []
        for hit in data.get("hits") or []:
            signal = hit.get("signal") or {}
            age = signal.get("bars_ago")
            if age is None or age >= delay:
                stale.append(hit)
        data["hits"] = stale[:5]
        data["elite"] = []
        data["delayed"] = True
        data["upgrade"] = "pro_hunter"
    else:
        data["delayed"] = False
    return data


@router.get("/confluence")
def confluence_endpoint(
    symbol: str = Query(default="BTC/USDT"),
    timeframes: str = Query(default="15m,1h,4h"),
    user: Optional[User] = Depends(access.optional_require("brain")),
) -> dict[str, Any]:
    tfs = [tf.strip() for tf in timeframes.split(",") if tf.strip()]
    try:
        return multi_timeframe(symbol, tfs)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/backtest")
def backtest_endpoint(
    symbol: str = Query(default="BTC/USDT"),
    timeframe: str = Query(default="15m"),
    horizon: int = Query(default=24, ge=4, le=200),
    reward_multiple: float = Query(default=2.0, ge=0.5, le=10.0),
    user: Optional[User] = Depends(access.optional_require("backtest")),
) -> dict[str, Any]:
    try:
        return backtest(symbol, timeframe, horizon, reward_multiple)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/correlation")
def correlation_endpoint(
    timeframe: str = Query(default="1h"),
    top: int = Query(default=12, ge=4, le=30),
    user: Optional[User] = Depends(access.optional_require("analytics")),
) -> dict[str, Any]:
    try:
        return correlation_matrix(timeframe, top)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/heatmap")
def heatmap_endpoint(
    symbol: str = Query(default="BTC/USDT"),
    timeframe: str = Query(default="1h"),
    user: Optional[User] = Depends(access.optional_require("analytics")),
) -> dict[str, Any]:
    try:
        return session_heatmap(symbol, timeframe)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/calibrate")
def calibrate_endpoint(
    symbols: str = Query(default=""),
    timeframes: str = Query(default="15m,1h"),
    top: int = Query(default=6, ge=1, le=20),
    horizon: int = Query(default=24, ge=4, le=200),
    reward_multiple: float = Query(default=2.0, ge=0.5, le=10.0),
    apply: bool = Query(default=False, description="persist the curve so live signals are mapped through it"),
    user: Optional[User] = Depends(access.optional_require("calibration")),
) -> dict[str, Any]:
    """Compare printed VRCS confidence against realised price movement."""
    if symbols.strip():
        universe = [s.strip() for s in symbols.split(",") if s.strip()]
    else:
        universe = [row["symbol"] for row in liquid_universe(top)]
    frames = [tf.strip() for tf in timeframes.split(",") if tf.strip()]
    reports = []
    errors = []
    for symbol in universe:
        for timeframe in frames:
            try:
                reports.append(backtest(symbol, timeframe, horizon, reward_multiple))
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{symbol} {timeframe}: {exc}")
    if not reports:
        raise HTTPException(status_code=502, detail="; ".join(errors) or "no data")
    result = calibrate(reports)
    result["symbols"] = universe
    result["timeframes"] = frames
    if errors:
        result["errors"] = errors[:10]
    if apply:
        result["applied_profile"] = save_profile(result)
    return result


@router.get("/calibration")
def calibration_profile(user: Optional[User] = Depends(access.optional_require("calibration"))) -> dict[str, Any]:
    profile = load_profile()
    return {"profile": profile, "applied": bool(profile)}


@router.get("/export.csv")
def export_csv(
    symbol: str = Query(default="BTC/USDT"),
    timeframe: str = Query(default="15m"),
    horizon: int = Query(default=24, ge=4, le=200),
    user: Optional[User] = Depends(access.optional_require("export")),
) -> StreamingResponse:
    try:
        report = backtest(symbol, timeframe, horizon)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["SHC VRCS report", symbol, timeframe, f"win_rate={report['win_rate']}%"])
    writer.writerow(
        ["time_utc", "side", "confidence", "entry", "stop", "target", "outcome", "bars_held", "pnl_pct", "streak", "volume_ratio"]
    )
    for trade in report["trades"]:
        writer.writerow(
            [
                trade["time"],
                trade["side"],
                trade["confidence"],
                trade["entry"],
                trade["stop"],
                trade["target"],
                trade["outcome"],
                trade["bars_held"],
                trade["pnl_pct"],
                trade["streak"],
                trade["volume_ratio"],
            ]
        )
    buffer.seek(0)
    filename = f"shc_{symbol.replace('/', '')}_{timeframe}.csv"
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
