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
    "chart": "الشارت الحي للعملات",
    "classic_indicators": "المؤشرات الكلاسيكية المجانية",
    "vrcs": "مؤشر SHC VRCS بالكامل",
    "live_equities": "تداول وأمريكا لحظة بلحظة",
    "delayed_equities": "أسهم ببيانات متأخرة",
    "hunter_delayed": "إشارات الصياد المتأخرة (محدودة)",
    "hunter": "الصياد الحي دون تأخير",
    "alerts": "تنبيهات 90%+ صوتية ومرئية",
    "watchlists": "قوائم المراقبة الذكية",
    "split2": "تقسيم إلى شارتين",
    "split4": "تقسيم إلى أربع شارتات",
    "brain": "توافق الفريمات (العقل)",
    "backtest": "الاختبار العكسي الفوري",
    "analytics": "الارتباط وخريطة الأوقات",
    "assistant": "المساعد الذكي داخل المنصة",
    "export": "تصدير التقارير",
    "webhooks": "تصدير الإشارات لحظياً (Webhooks)",
    "telegram": "تنبيهات Telegram والبريد الفوري",
    "calibration": "معايرة نسب الثقة",
    "execution_bot": "الوكيل التنفيذي الآلي",
    "auditor": "الوكيل المراقب الذكي",
}

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
        "tagline_ar": "شارت العملات والمؤشرات الكلاسيكية",
        "tagline_en": "Crypto chart and classic indicators",
        "price": 0,
        "days": 3650,
        "balance_credit": 0,
        "max_charts": 1,
        "scan_top": 8,
        "hunter_delay_bars": 8,
        "entitlements": ["chart", "classic_indicators", "delayed_equities", "hunter_delayed"],
        "features": [
            "عملات رقمية لحظية",
            "مؤشرات كلاسيكية (RSI, MACD, SMA, EMA, BB…)",
            "شارت واحد",
            "إشارات صياد متأخرة ومحدودة",
            "أسهم ببيانات متأخرة — بدون تنبيه لحظي",
        ],
        "locked": [
            "VRCS الكامل",
            "تداول وأمريكا الحي",
            "تنبيهات 90%+",
            "تقسيم الشاشة",
            "Webhooks / Telegram / المساعد",
        ],
    },
    {
        "id": PRO_HUNTER,
        "name_ar": "الصياد · Pro Hunter",
        "name_en": "Pro Hunter",
        "tagline_ar": "كل الأسواق + VRCS + تنبيهات 90%+",
        "tagline_en": "All markets, full VRCS, 90%+ alerts",
        "price": 49,
        "days": 30,
        "balance_credit": 100,
        "max_charts": 2,
        "scan_top": 40,
        "hunter_delay_bars": 0,
        "entitlements": [
            "chart",
            "classic_indicators",
            "vrcs",
            "live_equities",
            "hunter",
            "alerts",
            "watchlists",
            "split2",
            "brain",
            "execution_bot",
            "auditor",
        ],
        "features": [
            "كريبتو + تداول + أمريكا لحظياً",
            "VRCS بالكامل بلا قيود",
            "تنبيهات صوتية ومرئية 90%+",
            "شارتان + قوائم مراقبة ذكية",
            "توافق الفريمات (العقل)",
        ],
        "locked": ["4 شارتات", "Webhooks", "Telegram / بريد فوري", "المساعد الذكي", "الاختبار العكسي"],
    },
    {
        "id": ELITE_BRAIN,
        "name_ar": "العقل · Elite Brain",
        "name_en": "Elite Brain",
        "tagline_ar": "المنصة كاملة: أتمتة، ذكاء، و4 شارتات",
        "tagline_en": "Full desk: automation, AI, 4 charts",
        "price": 149,
        "days": 30,
        "balance_credit": 500,
        "max_charts": 4,
        "scan_top": 120,
        "hunter_delay_bars": 0,
        "entitlements": list(FEATURES.keys()),
        "features": [
            "كل ميزات الصياد",
            "4 شارتات متزامنة",
            "Webhooks لتصدير الإشارات لحظياً",
            "تنبيهات Telegram والبريد الفوري",
            "المساعد الذكي + الاختبار العكسي",
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
    return list(plan_of(user)["entitlements"])


def has_feature(user: User | None, feature: str) -> bool:
    if user is not None and getattr(user, "is_admin", False):
        return True
    return feature in plan_of(user)["entitlements"]


def allowed_indicators(user: User | None, ids: list[str]) -> list[str]:
    if has_feature(user, "vrcs"):
        return ids
    return [item for item in ids if item in CLASSIC_INDICATORS or item == "volume"]


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
    return {
        "subscription_tier": plan["id"],
        "plan": plan["id"],
        "effective_plan": plan["id"],
        "active": True if user is None else is_active_subscription(user),
        "days_left": days_left(user) if user else None,
        "expires_at": user.plan_expires_at.isoformat() if user and user.plan_expires_at else None,
        "entitlements": plan["entitlements"],
        "max_charts": plan["max_charts"],
        "scan_top": plan["scan_top"],
        "hunter_delay_bars": plan.get("hunter_delay_bars", 0),
        "email_verified": bool(user.email_verified) if user else False,
        "is_admin": bool(user and user.is_admin),
        "features_catalog": FEATURES,
        "classic_indicators": sorted(CLASSIC_INDICATORS),
    }
