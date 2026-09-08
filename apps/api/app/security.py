from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from apps.api.app.config import get_settings
from apps.api.app.db import get_session
from apps.api.app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
optional_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def is_platform_admin(email: str) -> bool:
    return (email or "").strip().lower() in get_settings().admin_email_list


def stamp_admin(user: User) -> bool:
    """Grant the founder/admin account full desk access. Returns True if the row changed."""
    if not user or not is_platform_admin(user.email):
        return False
    changed = False
    if not user.is_admin:
        user.is_admin = True
        changed = True
    if not user.is_active:
        user.is_active = True
        changed = True
    if not user.email_verified:
        user.email_verified = True
        changed = True
    if user.verify_token:
        user.verify_token = ""
        changed = True
    if user.subscription_tier != "elite_brain" or user.plan != "elite_brain":
        user.subscription_tier = "elite_brain"
        user.plan = "elite_brain"
        changed = True
    if user.plan_expires_at is not None:
        user.plan_expires_at = None
        changed = True
    if user.totp_enabled:
        user.totp_enabled = False
        user.totp_secret = ""
        user.totp_backup = ""
        changed = True
    return changed


def create_access_token(subject: str) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode(
        {"sub": subject, "exp": expire},
        settings.secret_key,
        algorithm="HS256",
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, get_settings().secret_key, algorithms=["HS256"])
        email = payload.get("sub")
        if not email:
            raise credentials_error
    except JWTError as exc:
        raise credentials_error from exc

    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not user.is_active:
        raise credentials_error
    if stamp_admin(user):
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def get_optional_user(
    token: Optional[str] = Depends(optional_oauth2),
    session: Session = Depends(get_session),
) -> Optional[User]:
    if not token:
        return None
    try:
        payload = jwt.decode(token, get_settings().secret_key, algorithms=["HS256"])
        email = payload.get("sub")
        if not email:
            return None
    except JWTError:
        return None
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not user.is_active:
        return None
    if stamp_admin(user):
        session.add(user)
        session.commit()
        session.refresh(user)
    return user
