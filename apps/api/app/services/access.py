"""SHC membership catalogue: explorer → pro_hunter → elite_brain."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from fastapi import Depends, HTTPException, status

from apps.api.app.models import User
from apps.api.app.security import get_current_user, get_optional_user

EXPLORER = "explorer"
PRO_HUNTER = "pro_hunter"
ELITE_BRAIN = "elite_brain"

LEGACY_TIERS = {
    "free": EXPLORER,
    "pro": PRO_HUNTER,
    "elite": ELITE_BRAIN,
}

FEATURES = {
    "chart": "الشارت الحي مع البحث والرسم",
    "classic_indicators": "كل المؤشرات عدا VRCS بصمة الاحتقان الصامت",
    "vrcs": "VRCS بصمة الاحتقان الصامت",
    "live_equities": "تداول وأمريكا لحظة بلحظة",
    "delayed_equities": "أسهم ببيانات متأخرة",
    "hunter_delayed": "إشارات الصياد المتأخرة (محدودة)",
    "hunter": "الصياد الحي دون تأخير",
    "alerts": "تنبيهات 90%+ صوتية ومرئية",
    "watchlists": "قوائم المراقبة الذكية",
    "split2": "تقسيم إلى شارتين",
    "split4": "تقسيم إلى أربع شارتات",
    "brain": "توافق الفريمات (العقل)",
    "agents": "وكلاء SHC",
    "backtest": "الاختبار العكسي الفوري",
    "analytics": "التحليلات",
    "assistant": "المساعد الذكي داخل المنصة",
    "export": "تصدير التقارير",
    "webhooks": "تصدير الإشارات لحظياً (Webhooks)",
    "telegram": "تنبيهات Telegram والبريد الفوري",
    "calibration": "معايرة نسب الثقة",
    "execution_bot": "الوكيل التنفيذي الآلي",
    "auditor": "الوكيل المراقب الذكي",
}

VRCS_ID = "vrcs"
CHART_BASE = [
    "chart",
    "classic_indicators",
    "live_equities",
    "delayed_equities",
    "watchlists",
    "split2",
]

CLASSIC_INDICATORS = {
    "volume",
    "sma20",
    "sma50",
    "sma200",
    "ema12",
    "ema26",
    "wma",
    "rsi",
    "macd",
    "stoch",
    "momentum",
    "bb",
}

PLANS: list[dict[str, Any]] = [
    {
        "id": EXPLORER,
        "name_ar": "الأساسية · Explorer",
        "name_en": "Explorer",
        "tagline_ar": "شارت كامل: بحث، رسم، وكل المؤشرات عدا VRCS",
        "tagline_en": "Full chart: search, drawing, and every indicator except VRCS",
        "price": 0,
        "days": 3650,
        "balance_credit": 0,
        "max_charts": 1,
        "scan_top": 8,
        "hunter_delay_bars": 8,
        "entitlements": list(CHART_BASE) + ["hunter_delayed"],
        "features": [
            "شارت حي مع البحث والرسم",
            "كل المؤشرات الفنية ما عدا VRCS بصمة الاحتقان الصامت",
            "أسواق العملات والأسهم",
        ],
        "locked": [
            "VRCS بصمة الاحتقان الصامت",
            "وكلاء SHC والتحليلات",
        ],
    },
    {
        "id": PRO_HUNTER,
        "name_ar": "الصياد · Pro Hunter",
        "name_en": "Pro Hunter",
        "tagline_ar": "VRCS بصمة الاحتقان الصامت مع تنبيهات الصياد",
        "tagline_en": "VRCS silent-congestion fingerprint plus hunter alerts",
        "price": 49,
        "days": 30,
        "balance_credit": 100,
        "max_charts": 2,
        "scan_top": 40,
        "hunter_delay_bars": 0,
        "entitlements": list(CHART_BASE)
        + [
            "vrcs",
            "hunter",
            "alerts",
            "brain",
            "execution_bot",
            "auditor",
        ],
        "features": [
            "كل ميزات الشارت الأساسية",
            "VRCS بصمة الاحتقان الصامت",
            "تنبيهات صوتية ومرئية 90%+",
            "شارتان + قوائم مراقبة ذكية",
        ],
        "locked": [
            "وكلاء SHC والتحليلات",
            "4 شارتات",
            "Webhooks / Telegram / المساعد",
        ],
    },
    {
        "id": ELITE_BRAIN,
        "name_ar": "العقل · Elite Brain",
        "name_en": "Elite Brain",
        "tagline_ar": "المنصة كاملة بما فيها وكلاء SHC والتحليلات",
        "tagline_en": "Full desk including SHC Agents and Analytics",
        "price": 149,
        "days": 30,
        "balance_credit": 500,
        "max_charts": 4,
        "scan_top": 120,
        "hunter_delay_bars": 0,
        "entitlements": list(FEATURES.keys()),
        "features": [
            "كل ميزات الصياد بما فيها VRCS",
            "وكلاء SHC والتحليلات",
            "4 شارتات متزامنة",
            "Webhooks وتلجرام والمساعد",
        ],
        "locked": [],
    },
]

PLAN_INDEX = {plan["id"]: plan for plan in PLANS}


def normalize_tier(value: str | None) -> str:
    raw = (value or EXPLORER).strip().lower()
    return LEGACY_TIERS.get(raw, raw if raw in PLAN_INDEX else EXPLORER)


def user_tier(user: User | None) -> str:
    if user is None:
        return EXPLORER
    if getattr(user, "is_admin", False):
        return ELITE_BRAIN
    stored = getattr(user, "subscription_tier", None) or getattr(user, "plan", None)
    return normalize_tier(stored)


def is_active_subscription(user: User) -> bool:
    if getattr(user, "is_admin", False):
        return True
    tier = user_tier(user)
    if tier == EXPLORER:
        return True
    if user.plan_expires_at is None:
        return True
    expires = user.plan_expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    return expires > datetime.now(timezone.utc)


def plan_of(user: User | None) -> dict[str, Any]:
    if user is None:
        return PLAN_INDEX[EXPLORER]
    tier = user_tier(user)
    if tier != EXPLORER and not is_active_subscription(user):
        return PLAN_INDEX[EXPLORER]
    return PLAN_INDEX.get(tier, PLAN_INDEX[EXPLORER])


def days_left(user: User) -> int | None:
    if user_tier(user) == EXPLORER or user.plan_expires_at is None:
        return None
    expires = user.plan_expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    return max(0, (expires - datetime.now(timezone.utc)).days)


def activate(user: User, plan_id: str) -> dict[str, Any]:
    tier = normalize_tier(plan_id)
    plan = PLAN_INDEX.get(tier)
    if not plan:
        raise HTTPException(status_code=400, detail="Unknown plan")
    now = datetime.now(timezone.utc)
    user.subscription_tier = tier
    user.plan = tier
    user.plan_started_at = now
    user.plan_expires_at = now + timedelta(days=int(plan["days"])) if tier != EXPLORER else None
    if tier != EXPLORER:
        user.balance = float(user.balance) + float(plan["balance_credit"])
    return plan


def entitlements(user: User | None) -> list[str]:
    if user is not None and getattr(user, "is_admin", False):
        return list(FEATURES.keys())
    return list(plan_of(user)["entitlements"])


def has_feature(user: User | None, feature: str) -> bool:
    if user is not None and getattr(user, "is_admin", False):
        return True
    return feature in plan_of(user)["entitlements"]


def allowed_indicators(user: User | None, ids: list[str]) -> list[str]:
    """Explorer gets every indicator except VRCS; paid plans include VRCS."""
    allow_vrcs = has_feature(user, "vrcs")
    return [item for item in ids if item != VRCS_ID or allow_vrcs]


def require_feature(feature: str):
    def guard(user: User = Depends(get_current_user)) -> User:
        if not has_feature(user, feature):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "upgrade_required", "feature": feature, "tier": user_tier(user)},
            )
        return user

    return guard


def require_any(*features: str):
    def guard(user: User = Depends(get_current_user)) -> User:
        if any(has_feature(user, feature) for feature in features):
            return user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "upgrade_required", "feature": features[0] if features else "alerts", "tier": user_tier(user)},
        )

    return guard


def optional_require(feature: str):
    """Same gate, but guests count as explorer."""

    def guard(user: Optional[User] = Depends(get_optional_user)) -> Optional[User]:
        if not has_feature(user, feature):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "upgrade_required", "feature": feature, "tier": user_tier(user)},
            )
        return user

    return guard


def access_summary(user: User | None) -> dict[str, Any]:
    plan = plan_of(user)
    admin = bool(user and user.is_admin)
    return {
        "subscription_tier": plan["id"],
        "plan": plan["id"],
        "effective_plan": plan["id"],
        "active": True if user is None else is_active_subscription(user),
        "days_left": days_left(user) if user else None,
        "expires_at": user.plan_expires_at.isoformat() if user and user.plan_expires_at else None,
        "entitlements": entitlements(user),
        "max_charts": plan["max_charts"],
        "scan_top": plan["scan_top"],
        "hunter_delay_bars": 0 if admin else plan.get("hunter_delay_bars", 0),
        "email_verified": bool(user.email_verified) if user else False,
        "is_admin": admin,
        "features_catalog": FEATURES,
        "classic_indicators": sorted(CLASSIC_INDICATORS),
    }
