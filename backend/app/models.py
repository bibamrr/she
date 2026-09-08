from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class PlanCode(str, Enum):
    FREE = "free"
    PRO = "pro"
    ELITE = "elite"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    display_name: str = "Trader"
    preferred_locale: str = "ar"
    plan: str = PlanCode.FREE.value
    balance: float = 0.0
    credits: int = 25
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Plan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(unique=True, index=True)
    name_en: str
    name_ar: str
    monthly_price: float
    credits_per_month: int
    max_watchlist: int
    agents_enabled: bool = True
