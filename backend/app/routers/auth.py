from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from sqlmodel import Session, select

from backend.app.db import get_session
from backend.app.deps import get_current_user
from backend.app.models import User
from backend.app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterBody(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    display_name: str = "Trader"
    preferred_locale: str = "ar"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    email: str
    display_name: str
    preferred_locale: str
    plan: str
    balance: float
    credits: int


@router.post("/register", response_model=TokenResponse)
def register(body: RegisterBody, session: Session = Depends(get_session)) -> TokenResponse:
    existing = session.exec(select(User).where(User.email == body.email.lower())).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = User(
        email=body.email.lower(),
        hashed_password=hash_password(body.password),
        display_name=body.display_name,
        preferred_locale=body.preferred_locale,
    )
    session.add(user)
    session.commit()
    return TokenResponse(access_token=create_access_token(user.email))


@router.post("/login", response_model=TokenResponse)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
) -> TokenResponse:
    user = session.exec(select(User).where(User.email == form.username.lower())).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(user.email))


class JsonLogin(BaseModel):
    email: EmailStr
    password: str


@router.post("/login-json", response_model=TokenResponse)
def login_json(body: JsonLogin, session: Session = Depends(get_session)) -> TokenResponse:
    user = session.exec(select(User).where(User.email == body.email.lower())).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(user.email))


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)) -> UserOut:
    return UserOut(
        email=user.email,
        display_name=user.display_name,
        preferred_locale=user.preferred_locale,
        plan=user.plan,
        balance=user.balance,
        credits=user.credits,
    )
