"""Hard caps for streaming market data so long-lived WS sessions stay bounded."""

from __future__ import annotations

import gc
import time
from pathlib import Path
from typing import Any, MutableMapping, Sequence, TypeVar

CANDLE_WINDOW = 1000
CACHE_MAX = 180
CACHE_STALE_SECONDS = 300
DISK_CANDLE_MAX_FILES = 80
DISK_CANDLE_MAX_AGE = 7 * 24 * 3600
TICKER_UNIVERSE_MAX = 400
MARK_CACHE_MAX = 200
LOGO_MEM_MAX = 200

_T = TypeVar("_T")


def clamp_limit(limit: int, default: int = 400) -> int:
    try:
        value = int(limit)
    except (TypeError, ValueError):
        value = default
    return max(1, min(value, CANDLE_WINDOW))


def tail(rows: Sequence[_T] | None, limit: int = CANDLE_WINDOW) -> list[_T]:
    if not rows:
        return []
    cap = clamp_limit(limit)
    if len(rows) <= cap:
        return list(rows)
    return list(rows[-cap:])


def prune_timed_cache(
    cache: MutableMapping[str, tuple[float, Any]],
    *,
    now: float | None = None,
    max_age: float = CACHE_STALE_SECONDS,
    max_items: int = CACHE_MAX,
) -> int:
    stamp = time.time() if now is None else now
    removed = 0
    for key, (when, _value) in list(cache.items()):
        if stamp - when > max_age:
            cache.pop(key, None)
            removed += 1
    while len(cache) > max_items:
        cache.pop(next(iter(cache)), None)
        removed += 1
    return removed


def prune_files(
    directory: Path,
    *,
    max_files: int = DISK_CANDLE_MAX_FILES,
    max_age: float = DISK_CANDLE_MAX_AGE,
) -> int:
    if not directory.exists():
        return 0
    now = time.time()
    removed = 0
    files = [path for path in directory.iterdir() if path.is_file()]
    for path in files:
        try:
            age = now - path.stat().st_mtime
        except OSError:
            continue
        if age > max_age:
            try:
                path.unlink()
                removed += 1
            except OSError:
                pass
    remaining = [path for path in directory.iterdir() if path.is_file()]
    if len(remaining) <= max_files:
        return removed
    remaining.sort(key=lambda path: path.stat().st_mtime)
    for path in remaining[: len(remaining) - max_files]:
        try:
            path.unlink()
            removed += 1
        except OSError:
            pass
    return removed


def collect() -> int:
    return gc.collect()


def sweep_runtime() -> dict[str, int]:
    """Drop unused caches and run a full GC. Safe to call every minute."""
    from apps.api.app.services import botday, logos, news, yahoo

    now = time.time()
    cleared = 0
    with yahoo._lock:
        cleared += prune_timed_cache(yahoo._cache, now=now)
    cleared += prune_timed_cache(news._CACHE, now=now, max_age=180, max_items=80)

    stamp, marks = botday._MARK_CACHE
    if now - stamp > 120:
        botday._MARK_CACHE = (0.0, {})
    elif len(marks) > MARK_CACHE_MAX:
        botday._MARK_CACHE = (stamp, dict(list(marks.items())[-MARK_CACHE_MAX:]))

    with logos._LOCK:
        for key, (when, *_rest) in list(logos._MEM.items()):
            if now - when > logos._TTL:
                logos._MEM.pop(key, None)
                cleared += 1
        while len(logos._MEM) > LOGO_MEM_MAX:
            logos._MEM.pop(next(iter(logos._MEM)), None)
            cleared += 1

    disk = prune_files(Path("data/candles"))
    return {
        "cache_cleared": cleared,
        "disk_cleared": disk,
        "gc": collect(),
    }
