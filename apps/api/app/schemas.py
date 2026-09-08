from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    display_name: str = ""
    locale: str = "ar"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    totp: Optional[str] = None


class ForgotRequest(BaseModel):
    email: EmailStr


class ResetRequest(BaseModel):
    token: str
    password: str = Field(min_length=8)


class TotpCodeRequest(BaseModel):
    code: str
    ticket: Optional[str] = None
    password: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserPublic(BaseModel):
    id: int
    email: str
    display_name: str
    locale: str
    plan: str
    subscription_tier: str = "explorer"
    balance: float
    email_verified: bool = False
    is_admin: bool = False
    totp_enabled: bool = False
    plan_expires_at: Optional[str] = None
    entitlements: List[str] = []
    max_charts: int = 1


class SubscribeRequest(BaseModel):
    plan: str


class AnalyzeRequest(BaseModel):
    symbol: str = "BTC/USDT"
    timeframe: str = "1h"
    lookback: int = Field(default=300, ge=20, le=1000)
    locale: Optional[str] = "ar"
