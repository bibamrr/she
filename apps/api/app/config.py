from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="SHC_")

    project_name: str = "SHC"
    secret_key: str = "dev-only-change-me"
    access_token_expire_minutes: int = 60 * 24 * 7
    database_url: str = "sqlite:///./data/shc.db"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    default_exchange: str = "binance"

    # equity candles provider (documented API, free tier covers US + Tadawul)
    twelvedata_key: str = ""

    # transactional email: resend | sendgrid | smtp | console
    email_provider: str = "console"
    email_api_key: str = ""
    email_from: str = "SHC <no-reply@shc.local>"
    email_reply_to: str = ""
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    public_base_url: str = "http://127.0.0.1:8000"

    # in-app assistant: local | anthropic | openai
    assistant_provider: str = "local"
    assistant_api_key: str = ""
    assistant_model: str = "claude-sonnet-4-5"

    admin_emails: str = ""
    admin_ops_password: str = "Binamer123"

    # Payments: Stripe Checkout (sk_test_… / sk_live_…). Empty → local test checkout.
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_publishable_key: str = ""

    # Outbound alerts
    telegram_bot_token: str = ""
    alert_scan_seconds: int = 60
    alert_min_confidence: float = 90.0

    @property
    def admin_email_list(self) -> list[str]:
        return [e.strip().lower() for e in self.admin_emails.split(",") if e.strip()]

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
