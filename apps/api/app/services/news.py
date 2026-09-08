"""Market news: Yahoo Finance + Google News RSS, cached per venue/symbol."""

from __future__ import annotations

import hashlib
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Optional

_CACHE: dict[str, tuple[float, list[dict[str, Any]]]] = {}
_TTL = 70.0
_UA = {
    "User-Agent": "Mozilla/5.0 (compatible; SHC-News/1.0; +https://shc.local)",
    "Accept": "application/rss+xml, application/json, text/xml, */*",
}

VENUE_QUERIES = {
    "crypto": {
        "ar": "عملات رقمية OR بيتكوين OR إيثريوم OR كريبتو",
        "en": "cryptocurrency OR bitcoin OR ethereum OR crypto market",
    },
    "tadawul": {
        "ar": "تداول OR السوق السعودي OR تاسي OR أرامكو",
        "en": "Tadawul OR Saudi stock exchange OR TASI OR Aramco",
    },
    "us": {
        "ar": "وول ستريت OR ناسداك OR أسهم أمريكا",
        "en": "Wall Street OR Nasdaq OR S&P 500 OR US stocks",
    },
    "europe": {
        "ar": "أسهم أوروبا OR داكس OR فوتسي OR يورو Stoxx",
        "en": "European stocks OR DAX OR FTSE OR Euro Stoxx",
    },
    "asia": {
        "ar": "أسهم آسيا OR نيكي OR هانغ سنغ OR توشي",
        "en": "Asian stocks OR Nikkei OR Hang Seng OR Tokyo stocks",
    },
    "commodities": {
        "ar": "الذهب OR النفط OR السلع OR خام برنت OR غاز طبيعي",
        "en": "gold OR crude oil OR commodities OR Brent OR natural gas",
    },
}

LOCALE_NEWS = {
    "ar": ("ar", "SA", "SA:ar"),
    "en": ("en-US", "US", "US:en"),
    "fr": ("fr", "FR", "FR:fr"),
    "zh": ("zh-CN", "CN", "CN:zh-Hans"),
    "ja": ("ja", "JP", "JP:ja"),
    "es": ("es", "ES", "ES:es"),
    "de": ("de", "DE", "DE:de"),
    "ko": ("ko", "KR", "KR:ko"),
    "ru": ("ru", "RU", "RU:ru"),
}


def yahoo_ticker(symbol: str) -> str:
    raw = (symbol or "").strip().upper().replace(" ", "")
    if "/" in raw:
        raw = raw.split(":", 1)[0]
        base, quote = raw.split("/", 1)
        if quote in {"USDT", "BUSD", "USD", "USDC", "FDUSD"}:
            return f"{base}-USD"
        return f"{base}-{quote}"
    return raw


SYMBOL_NAMES = {
    "BTC": {"en": ("Bitcoin",), "ar": ("بيتكوين", "Bitcoin")},
    "ETH": {"en": ("Ethereum",), "ar": ("إيثريوم", "Ethereum")},
    "SOL": {"en": ("Solana",), "ar": ("سولانا", "Solana")},
    "XRP": {"en": ("Ripple", "XRP"), "ar": ("ريبل", "XRP")},
    "BNB": {"en": ("Binance Coin", "BNB"), "ar": ("بينانس", "BNB")},
    "DOGE": {"en": ("Dogecoin",), "ar": ("دوجكوين", "Dogecoin")},
    "AAPL": {"en": ("Apple",), "ar": ("أبل", "Apple")},
    "TSLA": {"en": ("Tesla",), "ar": ("تسلا", "Tesla")},
    "MSFT": {"en": ("Microsoft",), "ar": ("مايكروسوفت", "Microsoft")},
    "NVDA": {"en": ("Nvidia",), "ar": ("إنفيديا", "Nvidia")},
    "AMZN": {"en": ("Amazon",), "ar": ("أمازون", "Amazon")},
    "2222": {"en": ("Aramco",), "ar": ("أرامكو",)},
    "1120": {"en": ("Al Rajhi",), "ar": ("الراجحي",)},
    "2010": {"en": ("SABIC",), "ar": ("سابك",)},
}


def _symbol_base(symbol: str) -> str:
    raw = (symbol or "").strip().upper().replace(" ", "")
    if "/" in raw:
        return raw.split("/", 1)[0]
    return raw.replace(".SR", "").split(".")[0]


def _symbol_needles(symbol: str) -> list[str]:
    raw = (symbol or "").strip().upper()
    base = _symbol_base(raw)
    tick = yahoo_ticker(raw)
    names: list[str] = [raw, base, tick, tick.replace("-", "")]
    for locale_pack in SYMBOL_NAMES.get(base, {}).values():
        names.extend(locale_pack)
    return [item for item in names if item]


def _symbol_query(symbol: str, locale: str) -> str:
    base = _symbol_base(symbol)
    tick = yahoo_ticker(symbol)
    aliases = list(SYMBOL_NAMES.get(base, {}).get(locale) or SYMBOL_NAMES.get(base, {}).get("en") or ())
    parts = [tick, base, *aliases]
    uniq: list[str] = []
    for part in parts:
        clean = str(part).strip()
        if clean and clean not in uniq:
            uniq.append(clean)
    return " OR ".join(f'"{part}"' if " " in part else part for part in uniq)


def _relevant_story(row: dict[str, Any], needles: list[str]) -> bool:
    hay = " ".join(
        [
            str(row.get("title") or ""),
            str(row.get("summary") or ""),
            " ".join(str(item) for item in (row.get("symbols") or [])),
        ]
    ).lower()
    return any(str(needle).lower() in hay for needle in needles if needle)


def _search_terms(venue: str, symbol: Optional[str], locale: str) -> str:
    pack = VENUE_QUERIES.get(venue, VENUE_QUERIES["crypto"])
    base = pack.get(locale) or pack["en"]
    if not symbol:
        return base
    return _symbol_query(symbol, locale)


def _get(url: str, timeout: float = 7.0) -> bytes:
    req = urllib.request.Request(url, headers=_UA)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _parse_time(value: Any) -> str:
    if value is None or value == "":
        return ""
    try:
        if isinstance(value, (int, float)):
            ts = float(value)
            if ts > 1e12:
                ts /= 1000.0
            return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
        text = str(value)
        try:
            return parsedate_to_datetime(text).astimezone(timezone.utc).isoformat()
        except (TypeError, ValueError):
            return text
    except (TypeError, ValueError, OSError):
        return str(value)


def _item_id(url: str, title: str) -> str:
    return hashlib.sha1(f"{url}|{title}".encode("utf-8", "ignore")).hexdigest()[:16]


def _yahoo_news(query: str) -> list[dict[str, Any]]:
    url = (
        "https://query1.finance.yahoo.com/v1/finance/search?"
        + urllib.parse.urlencode({"q": query, "quotesCount": 0, "newsCount": 20})
    )
    try:
        import json

        data = json.loads(_get(url).decode("utf-8", "replace"))
    except (urllib.error.URLError, TimeoutError, ValueError, OSError):
        return []
    out: list[dict[str, Any]] = []
    for row in data.get("news") or []:
        title = (row.get("title") or "").strip()
        link = row.get("link") or row.get("url") or ""
        if not title or not link:
            continue
        out.append(
            {
                "id": row.get("uuid") or _item_id(link, title),
                "title": title,
                "url": link,
                "source": row.get("publisher") or "Yahoo Finance",
                "published_at": _parse_time(row.get("providerPublishTime")),
                "symbols": [str(s) for s in (row.get("relatedTickers") or [])][:8],
                "summary": (row.get("summary") or "")[:280],
            }
        )
    return out


def _google_news(query: str, locale: str) -> list[dict[str, Any]]:
    hl, gl, ceid = LOCALE_NEWS.get(locale, LOCALE_NEWS["en"])
    url = "https://news.google.com/rss/search?" + urllib.parse.urlencode(
        {"q": query, "hl": hl, "gl": gl, "ceid": ceid}
    )
    try:
        raw = _get(url)
    except (urllib.error.URLError, TimeoutError, OSError):
        return []
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return []
    out: list[dict[str, Any]] = []
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if not title or not link:
            continue
        source_el = item.find("source")
        source = (source_el.text if source_el is not None and source_el.text else "Google News").strip()
        out.append(
            {
                "id": _item_id(link, title),
                "title": title,
                "url": link,
                "source": source,
                "published_at": _parse_time(item.findtext("pubDate")),
                "symbols": [],
                "summary": (item.findtext("description") or "")[:280],
            }
        )
    return out


def _dedupe(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for row in rows:
        key = (row.get("title") or "").lower()[:80]
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def fetch_news(
    venue: str = "crypto",
    symbol: Optional[str] = None,
    locale: str = "ar",
    limit: int = 36,
) -> dict[str, Any]:
    venue = venue if venue in VENUE_QUERIES else "crypto"
    locale = locale if locale in LOCALE_NEWS else "en"
    limit = max(4, min(int(limit or 36), 60))
    key = f"v2|{venue}|{symbol or ''}|{locale}|{limit}"
    now = time.time()
    hit = _CACHE.get(key)
    if hit and now - hit[0] < _TTL:
        return {"venue": venue, "symbol": symbol, "locale": locale, "items": hit[1][:limit], "cached": True}

    query = _search_terms(venue, symbol, locale)
    tick = yahoo_ticker(symbol) if symbol else ""
    rows: list[dict[str, Any]] = []
    needles = _symbol_needles(symbol) if symbol else []
    if tick:
        yahoo_rows = _yahoo_news(tick)
        rows.extend([row for row in yahoo_rows if not needles or _relevant_story(row, needles)])
    rows.extend(_google_news(query, locale))
    if symbol and locale != "en" and len(rows) < 8:
        rows.extend(_google_news(_symbol_query(symbol, "en"), "en"))
    if not symbol and len(rows) < 8:
        rows.extend(_google_news(_search_terms(venue, None, locale), locale))
    if symbol:
        focused = [row for row in rows if _relevant_story(row, needles)]
        rows = focused or rows
    items = _dedupe(rows)[:limit]
    _CACHE[key] = (now, items)
    if len(_CACHE) > 80:
        oldest = sorted(_CACHE.items(), key=lambda kv: kv[1][0])[:20]
        for stale, _ in oldest:
            _CACHE.pop(stale, None)
    return {"venue": venue, "symbol": symbol, "locale": locale, "items": items, "cached": False}
