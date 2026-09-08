from __future__ import annotations

from types import SimpleNamespace

from apps.api.app.services.access import (
    ELITE_BRAIN,
    EXPLORER,
    PRO_HUNTER,
    allowed_indicators,
    has_feature,
    plan_of,
    user_tier,
)


def _user(plan: str, admin: bool = False):
    return SimpleNamespace(
        is_admin=admin,
        subscription_tier=plan,
        plan=plan,
        plan_expires_at=None,
        email_verified=True,
    )


def test_explorer_locks_only_vrcs() -> None:
    user = _user(EXPLORER)
    assert has_feature(user, "chart")
    assert has_feature(user, "classic_indicators")
    assert has_feature(user, "live_equities")
    assert not has_feature(user, "vrcs")
    assert not has_feature(user, "agents")
    assert not has_feature(user, "analytics")
    assert allowed_indicators(user, ["rsi", "macd", "supertrend", "vrcs", "volume"]) == [
        "rsi",
        "macd",
        "supertrend",
        "volume",
    ]


def test_paid_plans_unlock_vrcs() -> None:
    hunter = _user(PRO_HUNTER)
    elite = _user(ELITE_BRAIN)
    assert has_feature(hunter, "vrcs")
    assert has_feature(elite, "vrcs")
    assert "vrcs" in allowed_indicators(hunter, ["vrcs", "rsi"])
    assert not has_feature(hunter, "agents")
    assert not has_feature(hunter, "analytics")


def test_elite_only_agents_and_analytics() -> None:
    elite = _user(ELITE_BRAIN)
    assert user_tier(elite) == ELITE_BRAIN
    assert has_feature(elite, "agents")
    assert has_feature(elite, "analytics")
    assert plan_of(elite)["id"] == ELITE_BRAIN


def test_admin_bypasses_plan_gates() -> None:
    admin = _user(EXPLORER, admin=True)
    assert user_tier(admin) == ELITE_BRAIN
    assert has_feature(admin, "vrcs")
    assert has_feature(admin, "agents")
    assert has_feature(admin, "analytics")
