from __future__ import annotations

from apps.api.app.services.memory import (
    CANDLE_WINDOW,
    CACHE_MAX,
    clamp_limit,
    prune_timed_cache,
    sweep_runtime,
    tail,
)


def test_clamp_limit_caps_at_window() -> None:
    assert clamp_limit(5000) == CANDLE_WINDOW
    assert clamp_limit(0) == 1
    assert clamp_limit(400) == 400


def test_tail_keeps_latest_window() -> None:
    rows = [[i, 1, 2, 3, 4, 5] for i in range(1500)]
    trimmed = tail(rows, 1000)
    assert len(trimmed) == CANDLE_WINDOW
    assert trimmed[0][0] == 500
    assert trimmed[-1][0] == 1499
    assert tail(rows[:10], 1000) == rows[:10]


def test_prune_timed_cache_drops_stale_and_overflow() -> None:
    cache = {f"k{i}": (1.0, i) for i in range(10)}
    cache["fresh"] = (10_180.0, "ok")
    removed = prune_timed_cache(cache, now=10_200.0, max_age=100, max_items=1)
    assert removed >= 10
    assert "fresh" in cache
    assert len(cache) == 1


def test_sweep_runtime_returns_counts() -> None:
    report = sweep_runtime()
    assert "cache_cleared" in report
    assert "gc" in report
    assert report["gc"] >= 0


def test_yahoo_cache_max_matches_shared_cap() -> None:
    from apps.api.app.services import yahoo

    assert yahoo._CACHE_MAX == CACHE_MAX
