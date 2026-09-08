from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Query

from apps.api.app.services.news import fetch_news

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("")
def list_news(
    venue: str = Query(default="crypto"),
    symbol: Optional[str] = Query(default=None),
    locale: str = Query(default="ar"),
    limit: int = Query(default=36, ge=4, le=60),
) -> dict:
    return fetch_news(venue=venue, symbol=symbol, locale=locale, limit=limit)
