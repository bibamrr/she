from __future__ import annotations
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

class RiskSettings(BaseModel):
    max_concurrent_positions: int = 3
    max_risk_per_trade_pct: float = 1.0

class Settings(BaseSettings):
    PROJECT_NAME: str = "Virtual Hedge Fund"
    environment: str = "development"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    binance_testnet: bool = True
    default_symbols: list[str] = ["BTC/USDT", "ETH/USDT"]
    default_timeframes: list[str] = ["1m", "5m"]
    risk: RiskSettings = Field(default_factory=RiskSettings)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

def get_settings() -> Settings:
    return Settings()
