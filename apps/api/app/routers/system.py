from __future__ import annotations

import asyncio
import gc
import json
import os
import platform
import resource
import subprocess
import time
import urllib.request
from typing import Any

from fastapi import APIRouter, Query

from apps.api.app.services import stocks
from apps.api.app.services.yahoo import _cache as upstream_cache

router = APIRouter(prefix="/api/system", tags=["system"])

_STARTED = time.time()
_BINANCE_PING = "https://api.binance.com/api/v3/time"


def _peak_rss_mb() -> float:
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # Linux reports kilobytes, macOS reports bytes
    divisor = 1024 * 1024 if platform.system() == "Darwin" else 1024
    return round(usage / divisor, 1)


def _current_rss_mb() -> float | None:
    """Resident set size right now — the number that reveals an actual leak."""
    try:
        with open("/proc/self/statm", encoding="utf-8") as handle:
            pages = int(handle.read().split()[1])
        return round(pages * os.sysconf("SC_PAGE_SIZE") / (1024 * 1024), 1)
    except OSError:
        pass
    try:
        out = subprocess.run(
            ["ps", "-o", "rss=", "-p", str(os.getpid())],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        value = out.stdout.strip()
        return round(int(value) / 1024, 1) if value.isdigit() else None
    except Exception:  # noqa: BLE001
        return None


@router.get("/diagnostics")
def diagnostics(probe: bool = Query(default=True)) -> dict[str, Any]:
    """Health snapshot: uptime, memory, server cache size and upstream latency."""
    report: dict[str, Any] = {
        "uptime_seconds": round(time.time() - _STARTED, 1),
        "pid": os.getpid(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "memory_rss_mb": _current_rss_mb(),
        "memory_peak_mb": _peak_rss_mb(),
        "server_cache_entries": len(upstream_cache),
        "stock_providers": stocks.provider_status(),
    }
    if probe:
        started = time.perf_counter()
        try:
            request = urllib.request.Request(_BINANCE_PING, headers={"User-Agent": "SHC/1.0"})
            with urllib.request.urlopen(request, timeout=8) as response:
                payload = json.loads(response.read().decode())
            report["binance"] = {
                "ok": True,
                "latency_ms": round((time.perf_counter() - started) * 1000, 1),
                "server_time": payload.get("serverTime"),
            }
        except Exception as exc:  # noqa: BLE001
            report["binance"] = {"ok": False, "error": str(exc)}
    return report


@router.post("/cache/clear")
def clear_cache() -> dict[str, Any]:
    removed = len(upstream_cache)
    upstream_cache.clear()
    gc.collect()
    return {"ok": True, "cleared": removed}


# ---------------------------------------------------------------- monitoring

_HISTORY: list[dict[str, Any]] = []
_HISTORY_MAX = 120
_SAMPLE_SECONDS = 60


def _sample() -> dict[str, Any]:
    entry = {
        "at": time.time(),
        "memory_rss_mb": _current_rss_mb(),
        "memory_peak_mb": _peak_rss_mb(),
        "cache_entries": len(upstream_cache),
    }
    started = time.perf_counter()
    try:
        request = urllib.request.Request(_BINANCE_PING, headers={"User-Agent": "SHC/1.0"})
        with urllib.request.urlopen(request, timeout=8):
            pass
        entry["upstream_latency_ms"] = round((time.perf_counter() - started) * 1000, 1)
    except Exception:  # noqa: BLE001
        entry["upstream_latency_ms"] = None
    _HISTORY.append(entry)
    while len(_HISTORY) > _HISTORY_MAX:
        _HISTORY.pop(0)
    return entry


async def monitor_loop() -> None:
    """Periodic cache + latency + memory sweep so slow leaks surface early."""
    while True:
        try:
            await asyncio.to_thread(_sample)
            now = time.time()
            stale = [k for k, (stamp, _) in list(upstream_cache.items()) if now - stamp > 900]
            for key in stale:
                upstream_cache.pop(key, None)
            if stale:
                gc.collect()
        except asyncio.CancelledError:
            raise
        except Exception:  # noqa: BLE001
            pass
        await asyncio.sleep(_SAMPLE_SECONDS)


@router.get("/history")
def history() -> dict[str, Any]:
    samples = list(_HISTORY)
    growth = None
    if len(samples) >= 2 and samples[0]["memory_rss_mb"] and samples[-1]["memory_rss_mb"]:
        growth = round(samples[-1]["memory_rss_mb"] - samples[0]["memory_rss_mb"], 1)
    latencies = [s["upstream_latency_ms"] for s in samples if s.get("upstream_latency_ms")]
    return {
        "samples": samples,
        "sample_seconds": _SAMPLE_SECONDS,
        "memory_growth_mb": growth,
        "avg_upstream_latency_ms": round(sum(latencies) / len(latencies), 1) if latencies else None,
        "leak_suspected": bool(growth is not None and growth > 400),
    }
