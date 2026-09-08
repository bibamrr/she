from __future__ import annotations

from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

from apps.api.app.config import get_settings

settings = get_settings()
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, echo=False, connect_args=connect_args)


_PAPER_POSITION_COLUMNS = {
    "source": "VARCHAR DEFAULT 'manual'",
    "confidence": "FLOAT DEFAULT 0",
    "timeframe": "VARCHAR DEFAULT ''",
    "venue": "VARCHAR DEFAULT ''",
    "signal_key": "VARCHAR DEFAULT ''",
}

_USER_COLUMNS = {
    "is_admin": "BOOLEAN DEFAULT 0",
    "email_verified": "BOOLEAN DEFAULT 0",
    "verify_token": "VARCHAR DEFAULT ''",
    "plan_started_at": "DATETIME",
    "plan_expires_at": "DATETIME",
    "last_login_at": "DATETIME",
    "subscription_tier": "VARCHAR DEFAULT 'explorer'",
    "webhook_url": "VARCHAR DEFAULT ''",
    "telegram_chat_id": "VARCHAR DEFAULT ''",
    "reset_token": "VARCHAR DEFAULT ''",
    "reset_expires_at": "DATETIME",
    "totp_secret": "VARCHAR DEFAULT ''",
    "totp_enabled": "BOOLEAN DEFAULT 0",
    "totp_backup": "VARCHAR DEFAULT ''",
}


def _migrate_sqlite() -> None:
    """Add columns introduced after a database file was already created."""
    with engine.connect() as connection:
        existing = {row[1] for row in connection.exec_driver_sql("PRAGMA table_info('user')")}
        if not existing:
            return
        for column, ddl in _USER_COLUMNS.items():
            if column not in existing:
                connection.exec_driver_sql(f"ALTER TABLE user ADD COLUMN {column} {ddl}")
        connection.exec_driver_sql(
            "UPDATE user SET subscription_tier = CASE "
            "WHEN plan IN ('elite','elite_brain') THEN 'elite_brain' "
            "WHEN plan IN ('pro','pro_hunter') THEN 'pro_hunter' "
            "ELSE 'explorer' END "
            "WHERE subscription_tier IS NULL OR subscription_tier IN ('','free','pro','elite')"
        )
        connection.exec_driver_sql(
            "UPDATE user SET plan = subscription_tier "
            "WHERE plan IN ('free','pro','elite') OR plan IS NULL OR plan = ''"
        )
        paper_cols = {row[1] for row in connection.exec_driver_sql("PRAGMA table_info('paperposition')")}
        if paper_cols:
            for column, ddl in _PAPER_POSITION_COLUMNS.items():
                if column not in paper_cols:
                    connection.exec_driver_sql(f"ALTER TABLE paperposition ADD COLUMN {column} {ddl}")
        accounts = {row[1] for row in connection.exec_driver_sql("PRAGMA table_info('paperaccount')")}
        if accounts:
            connection.exec_driver_sql(
                "UPDATE paperaccount SET cash = cash + (100000 - starting_cash), starting_cash = 100000 "
                "WHERE ABS(starting_cash - 100000) > 0.5"
            )
        connection.commit()


def _seed_founder_admin() -> None:
    from sqlmodel import Session, select

    from apps.api.app.models import User
    from apps.api.app.security import hash_password, stamp_admin, verify_password

    email = "bib.amrr@gmail.com"
    password = (get_settings().admin_password or "Asdfghas57").strip()
    if not email or not password:
        return
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if user is None:
            user = User(
                email=email,
                hashed_password=hash_password(password),
                display_name="عبدالاله",
                locale="ar",
            )
            session.add(user)
        elif not verify_password(password, user.hashed_password):
            user.hashed_password = hash_password(password)
        stamp_admin(user)
        session.add(user)
        session.commit()


def init_db() -> None:
    if settings.database_url.startswith("sqlite"):
        Path("data").mkdir(parents=True, exist_ok=True)
    from apps.api.app import models  # noqa: F401

    if settings.database_url.startswith("sqlite"):
        _migrate_sqlite()
    SQLModel.metadata.create_all(engine)
    if settings.database_url.startswith("sqlite"):
        _migrate_sqlite()
    _seed_founder_admin()


def get_session():
    with Session(engine) as session:
        yield session
