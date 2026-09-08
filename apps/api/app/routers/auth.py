from __future__ import annotations

import secrets
import time
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from apps.api.app.config import get_settings
from apps.api.app.db import get_session
from apps.api.app.models import User
from apps.api.app.schemas import (
    ForgotRequest,
    LoginRequest,
    RegisterRequest,
    ResetRequest,
    TokenResponse,
    TotpCodeRequest,
    UserPublic,
)
from apps.api.app.security import create_access_token, get_current_user, hash_password, verify_password
from apps.api.app.services import access, mailer, ratelimit, totp

router = APIRouter(prefix="/api/auth", tags=["auth"])

_LOGIN_TICKETS: dict[str, tuple[int, float]] = {}
_PENDING_TOTP: dict[int, str] = {}
_RESET_TTL = timedelta(hours=1)


def _verify_url(token: str) -> str:
    return f"{get_settings().public_base_url.rstrip('/')}/api/auth/verify?token={token}"


def _public(user: User) -> UserPublic:
    return UserPublic(
        id=user.id or 0,
        email=user.email,
        display_name=user.display_name,
        locale=user.locale,
        plan=access.plan_of(user)["id"],
        subscription_tier=access.plan_of(user)["id"],
        balance=user.balance,
        email_verified=user.email_verified,
        is_admin=user.is_admin,
        totp_enabled=bool(user.totp_enabled),
        plan_expires_at=user.plan_expires_at.isoformat() if user.plan_expires_at else None,
        entitlements=access.entitlements(user),
        max_charts=access.plan_of(user)["max_charts"],
    )


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, session: Session = Depends(get_session)) -> TokenResponse:
    email = payload.email.lower()
    existing = session.exec(select(User).where(User.email == email)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    locale = payload.locale if payload.locale in {"ar", "en"} else "ar"
    token = secrets.token_urlsafe(24)
    user = User(
        email=email,
        hashed_password=hash_password(payload.password),
        display_name=payload.display_name or email.split("@")[0],
        locale=locale,
        plan="explorer",
        subscription_tier="explorer",
        verify_token=token,
        is_admin=email in get_settings().admin_email_list,
    )
    session.add(user)
    session.commit()
    mailer.send_welcome(email, user.display_name, locale, _verify_url(token))
    return TokenResponse(access_token=create_access_token(user.email))


def _issue_token(session: Session, user: User) -> TokenResponse:
    user.last_login_at = datetime.now(timezone.utc)
    session.add(user)
    session.commit()
    return TokenResponse(access_token=create_access_token(user.email))


def _purge_tickets() -> None:
    now = time.time()
    for key, (_, exp) in list(_LOGIN_TICKETS.items()):
        if exp < now:
            _LOGIN_TICKETS.pop(key, None)


@router.post("/login")
def login(payload: LoginRequest, session: Session = Depends(get_session)) -> dict[str, Any]:
    email = payload.email.lower()
    if not ratelimit.allow(f"login:{email}", 8, 10 * 60):
        raise HTTPException(status_code=429, detail="Too many login attempts")
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not user.is_active or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if user.totp_enabled:
        if payload.totp:
            if totp.verify_code(user.totp_secret, payload.totp):
                token = _issue_token(session, user)
                return token.model_dump()
            leftover = totp.consume_backup(user.totp_backup, payload.totp)
            if leftover is not None:
                user.totp_backup = leftover
                token = _issue_token(session, user)
                return token.model_dump()
            raise HTTPException(status_code=401, detail="Invalid authenticator code")
        _purge_tickets()
        ticket = secrets.token_urlsafe(24)
        _LOGIN_TICKETS[ticket] = (user.id or 0, time.time() + 300)
        return {"requires_2fa": True, "ticket": ticket}
    token = _issue_token(session, user)
    return token.model_dump()


@router.post("/2fa/verify")
def verify_login_2fa(payload: TotpCodeRequest, session: Session = Depends(get_session)) -> TokenResponse:
    _purge_tickets()
    ticket = (payload.ticket or "").strip()
    row = _LOGIN_TICKETS.get(ticket)
    if not row:
        raise HTTPException(status_code=401, detail="2FA session expired")
    user = session.get(User, row[0])
    if not user or not user.totp_enabled:
        raise HTTPException(status_code=401, detail="Invalid 2FA session")
    if totp.verify_code(user.totp_secret, payload.code):
        _LOGIN_TICKETS.pop(ticket, None)
        return _issue_token(session, user)
    leftover = totp.consume_backup(user.totp_backup, payload.code)
    if leftover is None:
        raise HTTPException(status_code=401, detail="Invalid authenticator code")
    user.totp_backup = leftover
    _LOGIN_TICKETS.pop(ticket, None)
    return _issue_token(session, user)


@router.post("/forgot")
def forgot(payload: ForgotRequest, session: Session = Depends(get_session)) -> dict[str, Any]:
    email = payload.email.lower()
    if not ratelimit.allow(f"forgot:{email}", 3, 15 * 60):
        return {"ok": True}
    user = session.exec(select(User).where(User.email == email)).first()
    if user and user.is_active:
        token = secrets.token_urlsafe(32)
        user.reset_token = token
        user.reset_expires_at = datetime.now(timezone.utc) + _RESET_TTL
        session.add(user)
        session.commit()
        reset_url = f"{get_settings().public_base_url.rstrip('/')}/#/reset?token={token}"
        mailer.send_reset(user.email, user.display_name, user.locale, reset_url)
    return {"ok": True}


@router.post("/reset")
def reset_password(payload: ResetRequest, session: Session = Depends(get_session)) -> dict[str, Any]:
    token = (payload.token or "").strip()
    if not token or not ratelimit.allow(f"reset:{token[:12]}", 6, 15 * 60):
        raise HTTPException(status_code=400, detail="Invalid or expired reset link")
    user = session.exec(select(User).where(User.reset_token == token)).first()
    now = datetime.now(timezone.utc)
    expires = user.reset_expires_at if user else None
    if expires and expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    if not user or not expires or expires < now:
        raise HTTPException(status_code=400, detail="Invalid or expired reset link")
    user.hashed_password = hash_password(payload.password)
    user.reset_token = ""
    user.reset_expires_at = None
    session.add(user)
    session.commit()
    return {"ok": True}


@router.get("/reset", response_class=HTMLResponse)
def reset_page(token: str = Query(default="")) -> HTMLResponse:
    base = get_settings().public_base_url.rstrip("/")
    target = f"{base}/#/reset?token={token}" if token else f"{base}/#/auth"
    return HTMLResponse(
        "<body style='background:#05070a;color:#e8edf4;font-family:sans-serif;padding:40px;text-align:center'>"
        "<h2 style='color:#c8a45a'>SHC</h2>"
        f"<p><a style='color:#c8a45a' href='{target}'>متابعة تعيين كلمة المرور · Continue reset</a></p></body>"
    )


@router.get("/2fa/status")
def totp_status(user: User = Depends(get_current_user)) -> dict[str, Any]:
    return {"enabled": bool(user.totp_enabled)}


@router.post("/2fa/setup")
def totp_setup(user: User = Depends(get_current_user)) -> dict[str, Any]:
    if user.totp_enabled:
        raise HTTPException(status_code=400, detail="Authenticator already enabled")
    secret = totp.new_secret()
    _PENDING_TOTP[user.id or 0] = secret
    return {"secret": secret, "otpauth_url": totp.otpauth_uri(secret, user.email), "enabled": False}


@router.post("/2fa/enable")
def totp_enable(
    payload: TotpCodeRequest,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    secret = _PENDING_TOTP.get(user.id or 0)
    if not secret:
        raise HTTPException(status_code=400, detail="Start authenticator setup first")
    if not totp.verify_code(secret, payload.code):
        raise HTTPException(status_code=400, detail="Invalid authenticator code")
    codes = totp.new_backup_codes()
    user.totp_secret = secret
    user.totp_enabled = True
    user.totp_backup = ",".join(totp.hash_backup(code) for code in codes)
    session.add(user)
    session.commit()
    _PENDING_TOTP.pop(user.id or 0, None)
    return {"ok": True, "enabled": True, "backup_codes": codes}


@router.post("/2fa/disable")
def totp_disable(
    payload: TotpCodeRequest,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    if not user.totp_enabled:
        return {"ok": True, "enabled": False}
    password_ok = bool(payload.password) and verify_password(payload.password or "", user.hashed_password)
    code_ok = totp.verify_code(user.totp_secret, payload.code)
    leftover = totp.consume_backup(user.totp_backup, payload.code)
    if not (password_ok and (code_ok or leftover is not None)):
        raise HTTPException(status_code=401, detail="Password and authenticator code required")
    user.totp_secret = ""
    user.totp_enabled = False
    user.totp_backup = ""
    session.add(user)
    session.commit()
    return {"ok": True, "enabled": False}


@router.get("/me", response_model=UserPublic)
def me(user: User = Depends(get_current_user)) -> UserPublic:
    return _public(user)


@router.get("/verify", response_class=HTMLResponse)
def verify(token: str = Query(...), session: Session = Depends(get_session)) -> HTMLResponse:
    user = session.exec(select(User).where(User.verify_token == token)).first()
    if not user or not token:
        return HTMLResponse(
            "<body style='background:#05070a;color:#ef5350;font-family:sans-serif;padding:40px'>"
            "رابط التفعيل غير صالح — Invalid activation link</body>",
            status_code=400,
        )
    if not user.email_verified:
        user.email_verified = True
        user.verify_token = ""
        session.add(user)
        session.commit()
        mailer.send_verified(user.email, user.display_name, user.locale)
    base = get_settings().public_base_url
    return HTMLResponse(
        "<body style='background:#05070a;color:#e8edf4;font-family:sans-serif;padding:40px;text-align:center'>"
        "<h2 style='color:#c8a45a'>تم تفعيل الحساب · Account verified</h2>"
        f"<p><a style='color:#c8a45a' href='{base}'>افتح منصة SHC</a></p></body>"
    )


@router.post("/resend-verification")
def resend_verification(user: User = Depends(get_current_user), session: Session = Depends(get_session)) -> dict[str, Any]:
    if user.email_verified:
        return {"ok": True, "already_verified": True}
    user.verify_token = user.verify_token or secrets.token_urlsafe(24)
    session.add(user)
    session.commit()
    result = mailer.send_welcome(user.email, user.display_name, user.locale, _verify_url(user.verify_token))
    return {"ok": result["ok"], "provider": result["provider"]}


@router.get("/access")
def access_state(user: User = Depends(get_current_user)) -> dict[str, Any]:
    return access.access_summary(user)
