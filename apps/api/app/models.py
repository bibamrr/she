from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    display_name: str = ""
    locale: str = "ar"
    plan: str = "explorer"
    subscription_tier: str = "explorer"
    webhook_url: str = ""
    telegram_chat_id: str = ""
    balance: float = 0.0
    is_active: bool = True
    created_at: datetime = Field(default_factory=_utcnow)
    is_admin: bool = False
    email_verified: bool = False
    verify_token: str = ""
    plan_started_at: Optional[datetime] = None
    plan_expires_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    reset_token: str = ""
    reset_expires_at: Optional[datetime] = None
    totp_secret: str = ""
    totp_enabled: bool = False
    totp_backup: str = ""


class PaymentSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    token: str = Field(index=True, unique=True)
    user_id: int = Field(index=True)
    plan: str
    amount_cents: int = 0
    currency: str = "usd"
    provider: str = "test"
    provider_ref: str = ""
    status: str = "pending"
    created_at: datetime = Field(default_factory=_utcnow)
    paid_at: Optional[datetime] = None


class AlertDelivery(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    dedupe_key: str = Field(index=True)
    symbol: str
    timeframe: str = ""
    channel: str
    ok: bool = True
    detail: str = ""
    created_at: datetime = Field(default_factory=_utcnow)


class PaperAccount(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, unique=True)
    cash: float = 100000.0
    starting_cash: float = 100000.0
    updated_at: datetime = Field(default_factory=_utcnow)


class PaperPosition(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    symbol: str = Field(index=True)
    side: str = "long"
    qty: float = 0.0
    entry: float = 0.0
    stop: float = 0.0
    target: float = 0.0
    status: str = Field(default="open", index=True)
    exit: Optional[float] = None
    pnl: float = 0.0
    reason: str = ""
    source: str = "manual"
    confidence: float = 0.0
    timeframe: str = ""
    venue: str = ""
    signal_key: str = Field(default="", index=True)
    opened_at: datetime = Field(default_factory=_utcnow)
    closed_at: Optional[datetime] = None


class AgentDesk(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, unique=True)
    execution_enabled: bool = True
    min_confidence: float = 88.0
    max_open: int = 6
    risk_pct: float = 1.0
    venue: str = "auto"
    last_tick_at: Optional[datetime] = None
    last_audit_at: Optional[datetime] = None
    params_json: str = "{}"
    updated_at: datetime = Field(default_factory=_utcnow)


class AgentReport(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    kind: str = Field(default="execution", index=True)
    title: str = ""
    body: str = ""
    created_at: datetime = Field(default_factory=_utcnow)


class BotDay(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    day: str = Field(index=True, unique=True)
    opened: int = 0
    wins: int = 0
    losses: int = 0
    profit: float = 0.0
    loss: float = 0.0
    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0
    wallet: float = 100000.0
    reset_at: datetime = Field(default_factory=_utcnow)
    created_at: datetime = Field(default_factory=_utcnow)


class SwarmReview(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    signal_key: str = Field(index=True, unique=True)
    symbol: str = Field(index=True)
    timeframe: str = ""
    venue: str = ""
    side: str = ""
    hunter_confidence: float = 0.0
    entry: float = 0.0
    stop: float = 0.0
    target: float = 0.0
    status: str = Field(default="pending", index=True)
    votes_for: int = 0
    votes_against: int = 0
    direction: str = ""
    success_probability: float = 0.0
    agents_json: str = "[]"
    body_json: str = "{}"
    created_at: datetime = Field(default_factory=_utcnow)
    reviewed_at: Optional[datetime] = None


class WatchItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    symbol: str = Field(index=True)
    position: int = 0
    created_at: datetime = Field(default_factory=_utcnow)
