"""Anonymous TradingView chart websocket — used when Yahoo / Twelve Data are unavailable.

This is the same public chart protocol the Tadawul desk already uses for quotes
via scanner.tradingview.com. History is not an official SLA'd API; treat it as
a soft fallback and cache whatever it returns.
"""

from __future__ import annotations

import json
import random
import string
import threading
import time
from typing import Any

from websockets.sync.client import connect

from apps.api.app.services.memory import clamp_limit, tail

_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
_WS = "wss://data.tradingview.com/socket.io/websocket"
_LOCK = threading.Lock()

_RES = {
    "1s": "1",
    "1m": "1",
    "3m": "3",
    "5m": "5",
    "15m": "15",
    "30m": "30",
    "1h": "60",
    "2h": "120",
    "4h": "240",
    "6h": "1D",
    "12h": "1D",
    "1d": "1D",
    "3d": "1D",
    "1w": "1W",
    "1M": "1M",
    "1Y": "1M",
}


def _sid(prefix: str) -> str:
    return prefix + "".join(random.choice(string.ascii_lowercase) for _ in range(12))


def _frame(func: str, params: list[Any]) -> str:
    body = json.dumps({"m": func, "p": params}, separators=(",", ":"))
    return f"~m~{len(body)}~m~{body}"


def _parts(raw: str) -> list[str]:
    out: list[str] = []
    index = 0
    while True:
        start = raw.find("~m~", index)
        if start < 0:
            if raw and not out:
                out.append(raw)
            break
        start += 3
        mid = raw.find("~m~", start)
        if mid < 0:
            break
        try:
            size = int(raw[start:mid])
        except ValueError:
            break
        out.append(raw[mid + 3 : mid + 3 + size])
        index = mid + 3 + size
    return out


def _bars_from_payload(payload: Any, rows: list[list[Any]]) -> None:
    if not isinstance(payload, dict):
        return
    series = payload.get("sds_1") or payload.get("s1") or {}
    if isinstance(series, dict):
        for item in series.get("s") or []:
            values = item.get("v") if isinstance(item, dict) else None
            if not values or len(values) < 5:
                continue
            try:
                ts = int(float(values[0]) * 1000)
                open_, high, low, close = (float(values[1]), float(values[2]), float(values[3]), float(values[4]))
                volume = float(values[5]) if len(values) > 5 and values[5] is not None else 0.0
            except (TypeError, ValueError):
                continue
            if ts <= 0 or close <= 0:
                continue
            rows.append([ts, open_, high, low, close, volume])
    for value in payload.values():
        if isinstance(value, dict) and ("sds_1" in value or "s1" in value or "s" in value):
            _bars_from_payload(value, rows)


def tv_ohlcv(tv_symbol: str, timeframe: str, limit: int = 300, timeout: float = 14.0) -> list[list[Any]]:
    """Fetch OHLCV for an ``EXCHANGE:TICKER`` symbol over the public chart socket."""
    if not tv_symbol:
        raise RuntimeError("missing TradingView symbol")
    limit = clamp_limit(limit)
    resolution = _RES.get(timeframe, "1D")
    chart = _sid("cs_")
    symbol_spec = json.dumps(
        {"symbol": tv_symbol, "adjustment": "splits", "session": "regular"},
        separators=(",", ":"),
    )
    rows: list[list[Any]] = []
    completed = False
    with _LOCK:
        with connect(
            _WS,
            origin="https://www.tradingview.com",
            additional_headers={"User-Agent": _UA},
            user_agent_header=_UA,
            open_timeout=min(10.0, timeout),
            close_timeout=2,
            max_size=8_000_000,
            ping_interval=None,
        ) as ws:
            ws.send(_frame("set_auth_token", ["unauthorized_user_token"]))
            ws.send(_frame("chart_create_session", [chart, ""]))
            ws.send(_frame("resolve_symbol", [chart, "sds_sym_1", f"={symbol_spec}"]))
            ws.send(_frame("create_series", [chart, "sds_1", "s1", "sds_sym_1", resolution, int(limit)]))
            deadline = time.time() + timeout
            while time.time() < deadline:
                try:
                    raw = ws.recv(timeout=max(0.3, deadline - time.time()))
                except Exception:
                    break
                if not raw:
                    continue
                text = raw.decode("utf-8", "ignore") if isinstance(raw, (bytes, bytearray)) else str(raw)
                for part in _parts(text):
                    if part.startswith("~h~"):
                        echo = f"~m~{len(part)}~m~{part}"
                        try:
                            ws.send(echo)
                        except Exception:
                            pass
                        continue
                    try:
                        message = json.loads(part)
                    except json.JSONDecodeError:
                        continue
                    kind = message.get("m")
                    params = message.get("p") or []
                    if kind in {"timescale_update", "du"} and len(params) >= 2:
                        _bars_from_payload(params[1], rows)
                    if kind == "series_completed":
                        completed = True
                if completed and rows:
                    break
    if not rows:
        raise RuntimeError(f"No TradingView history for {tv_symbol}")
    by_ts: dict[int, list[Any]] = {int(row[0]): row for row in rows}
    ordered = [by_ts[key] for key in sorted(by_ts)]
    return tail(ordered, limit)
