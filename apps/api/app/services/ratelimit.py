"""In-process request throttle for auth endpoints."""

from __future__ import annotations

import time
from threading import Lock

_hits: dict[str, list[float]] = {}
_lock = Lock()


def allow(key: str, limit: int, window: float) -> bool:
    now = time.time()
    with _lock:
        recent = [stamp for stamp in _hits.get(key, []) if now - stamp < window]
        if len(recent) >= limit:
            _hits[key] = recent
            return False
        recent.append(now)
        _hits[key] = recent
        if len(_hits) > 4000:
            stale = [name for name, stamps in _hits.items() if not stamps or now - stamps[-1] > window]
            for name in stale[:800]:
                _hits.pop(name, None)
        return True
