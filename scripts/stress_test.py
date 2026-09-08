#!/usr/bin/env python3
"""SHC stress and stability probe.

Measures REST latency under concurrency, WebSocket tick latency, and whether the
API process leaks memory across the run.

    python scripts/stress_test.py --rounds 3 --concurrency 8
"""

from __future__ import annotations

import argparse
import asyncio
import json
import statistics
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from typing import Any

DEFAULT_BASE = "http://127.0.0.1:8000"
BINANCE_WS = "wss://stream.binance.com:9443/stream?streams=btcusdt@kline_1m/btcusdt@miniTicker"

ENDPOINTS = [
    "/api/health",
    "/api/market/symbols",
    "/api/indicators/catalog",
    "/api/indicators/compute?symbol=BTC/USDT&timeframe=15m&ids=vrcs,volume,rsi,adx&limit=300",
    "/api/market/scan?venue=crypto",
    "/api/market/scan?venue=tadawul",
    "/api/market/scan?venue=us",
    "/api/hunter/confluence?symbol=BTC/USDT&timeframes=15m,1h",
    "/api/hunter/heatmap?symbol=BTC/USDT&timeframe=1h",
    "/api/system/diagnostics?probe=false",
]


def fetch(base: str, path: str, timeout: int = 90) -> dict[str, Any]:
    started = time.perf_counter()
    url = base + path
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "SHC-stress/1.0"})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read()
        return {
            "path": path,
            "ok": True,
            "status": response.status,
            "ms": (time.perf_counter() - started) * 1000,
            "bytes": len(payload),
        }
    except urllib.error.HTTPError as exc:
        return {"path": path, "ok": False, "status": exc.code, "ms": (time.perf_counter() - started) * 1000}
    except Exception as exc:  # noqa: BLE001
        return {"path": path, "ok": False, "status": 0, "error": str(exc), "ms": (time.perf_counter() - started) * 1000}


def diagnostics(base: str) -> dict[str, Any]:
    try:
        request = urllib.request.Request(base + "/api/system/diagnostics?probe=false")
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode())
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


def rest_phase(base: str, rounds: int, concurrency: int) -> dict[str, Any]:
    jobs = [path for _ in range(rounds) for path in ENDPOINTS]
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        results = list(pool.map(lambda p: fetch(base, p), jobs))

    per_path: dict[str, list[float]] = {}
    for row in results:
        per_path.setdefault(row["path"], []).append(row["ms"])

    summary = []
    for path, samples in per_path.items():
        samples.sort()
        summary.append(
            {
                "path": path,
                "calls": len(samples),
                "p50_ms": round(statistics.median(samples), 1),
                "p95_ms": round(samples[max(0, int(len(samples) * 0.95) - 1)], 1),
                "max_ms": round(samples[-1], 1),
            }
        )
    summary.sort(key=lambda r: r["p95_ms"], reverse=True)
    failures = [r for r in results if not r["ok"]]
    return {"summary": summary, "calls": len(results), "failures": failures}


async def ws_phase(seconds: int) -> dict[str, Any]:
    try:
        import websockets
    except ImportError:
        return {"skipped": "websockets package not installed"}

    latencies: list[float] = []
    messages = 0
    started = time.time()
    try:
        async with websockets.connect(BINANCE_WS, open_timeout=15, ping_interval=20) as socket:
            connect_ms = (time.time() - started) * 1000
            while time.time() - started < seconds:
                try:
                    raw = await asyncio.wait_for(socket.recv(), timeout=10)
                except asyncio.TimeoutError:
                    break
                messages += 1
                try:
                    payload = json.loads(raw).get("data", {})
                except json.JSONDecodeError:
                    continue
                event_time = payload.get("E")
                if event_time:
                    latencies.append(time.time() * 1000 - float(event_time))
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc), "messages": messages}

    latencies = [x for x in latencies if -5000 < x < 60000]
    return {
        "ok": True,
        "connect_ms": round(connect_ms, 1),
        "messages": messages,
        "msgs_per_sec": round(messages / max(seconds, 1), 2),
        "latency_p50_ms": round(statistics.median(latencies), 1) if latencies else None,
        "latency_max_ms": round(max(latencies), 1) if latencies else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default=DEFAULT_BASE)
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument("--concurrency", type=int, default=8)
    parser.add_argument("--ws-seconds", type=int, default=15)
    args = parser.parse_args()

    before = diagnostics(args.base)
    print(f"SHC stress probe → {args.base}")
    print(
        f"  memory before: {before.get('memory_rss_mb')} MB (peak {before.get('memory_peak_mb')})"
        f" · server cache: {before.get('server_cache_entries')}"
    )

    rest = rest_phase(args.base, args.rounds, args.concurrency)
    print(f"\nREST: {rest['calls']} calls, {len(rest['failures'])} failures")
    for row in rest["summary"]:
        print(f"  p50 {row['p50_ms']:>8.1f}ms  p95 {row['p95_ms']:>8.1f}ms  {row['path']}")
    for failure in rest["failures"][:5]:
        print(f"  FAIL {failure['status']} {failure['path']} {failure.get('error', '')}")

    ws = asyncio.run(ws_phase(args.ws_seconds))
    print("\nWebSocket (Binance live feed):")
    for key, value in ws.items():
        print(f"  {key}: {value}")

    after = diagnostics(args.base)
    growth = None
    if before.get("memory_rss_mb") and after.get("memory_rss_mb"):
        growth = round(after["memory_rss_mb"] - before["memory_rss_mb"], 1)
    print("\nStability:")
    print(
        f"  memory after: {after.get('memory_rss_mb')} MB (growth {growth} MB,"
        f" peak {after.get('memory_peak_mb')} MB)"
    )
    print(f"  server cache entries: {after.get('server_cache_entries')}")
    verdict = "OK"
    if rest["failures"]:
        verdict = "REST FAILURES"
    elif growth is not None and growth > 150:
        verdict = "POSSIBLE MEMORY LEAK"
    elif ws.get("ok") is False:
        verdict = "WS UNREACHABLE"
    print(f"  verdict: {verdict}")


if __name__ == "__main__":
    main()
