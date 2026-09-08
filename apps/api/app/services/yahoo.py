from __future__ import annotations

import http.cookiejar
import json
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

_cache: dict[str, tuple[float, Any]] = {}
_lock = threading.Lock()
_UA = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json,text/plain,*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://finance.yahoo.com/",
}

_session_lock = threading.Lock()
_rate_lock = threading.Lock()
_opener: urllib.request.OpenerDirector | None = None
_crumb = ""
_session_at = 0.0
_last_request = 0.0
_SESSION_TTL = 45 * 60
_MIN_GAP = 1.15

SAUDI_UNIVERSE = [
    ("2222.SR", "أرامكو"),
    ("1120.SR", "الراجحي"),
    ("2010.SR", "سابك"),
    ("1180.SR", "الأهلي"),
    ("1150.SR", "الإنماء"),
    ("1010.SR", "الرياض"),
    ("1050.SR", "الفرنسي"),
    ("1060.SR", "ساب"),
    ("1140.SR", "البلاد"),
    ("1080.SR", "العربي"),
    ("7010.SR", "اس تي سي"),
    ("7020.SR", "إتحاد إتصالات"),
    ("7030.SR", "زين"),
    ("1211.SR", "معادن"),
    ("1320.SR", "الأنابيب"),
    ("2020.SR", "سافكو"),
    ("2290.SR", "ينساب"),
    ("2350.SR", "كيان"),
    ("2380.SR", "بترورابغ"),
    ("1202.SR", "مبكو"),
    ("4001.SR", "أسواق العثيم"),
    ("4003.SR", "إكسترا"),
    ("4190.SR", "جرير"),
    ("1210.SR", "بي سي آي"),
    ("1303.SR", "صناعات كهربائية"),
    ("1830.SR", "وقت اللياقة"),
    ("2280.SR", "المراعي"),
    ("2270.SR", "سدافكو"),
    ("6001.SR", "حلواني"),
    ("1810.SR", "سيرا"),
    ("1820.SR", "الحكير"),
    ("4300.SR", "دار الأركان"),
    ("4310.SR", "مدينة المعرفة"),
    ("5110.SR", "كهرباء السعودية"),
    ("2082.SR", "أكوا باور"),
    ("7203.SR", "علم"),
    ("7202.SR", "سلوشنز"),
    ("4263.SR", "سال"),
    ("4261.SR", "ذيب"),
    ("4030.SR", "البحري"),
]


_CACHE_MAX = 240

_EURO_SFX = (".L", ".PA", ".DE", ".AS", ".MI", ".SW", ".MC")
_ASIA_SFX = (".T", ".HK", ".KS", ".KQ", ".SS", ".SZ", ".AX", ".TW", ".NS", ".BO")


def _guess_venue(symbol: Any) -> str:
    clean = str(symbol or "").upper().strip()
    if "/" in clean:
        return "crypto"
    if clean.endswith("=F"):
        return "commodities"
    if clean.endswith(".SR") or clean.replace(".SR", "").isdigit():
        return "tadawul"
    if any(clean.endswith(sfx) for sfx in _EURO_SFX):
        return "europe"
    if any(clean.endswith(sfx) for sfx in _ASIA_SFX):
        return "asia"
    return "us"


def _cached(key: str, ttl: float, loader):
    now = time.time()
    with _lock:
        hit = _cache.get(key)
        if hit and now - hit[0] < ttl:
            return hit[1]
    value = loader()
    with _lock:
        _cache[key] = (now, value)
        # drop stale entries, then cap the dict so long sessions cannot creep upward
        for stale_key in [k for k, (stamp, _) in _cache.items() if now - stamp > max(ttl, 600)]:
            _cache.pop(stale_key, None)
        while len(_cache) > _CACHE_MAX:
            _cache.pop(next(iter(_cache)), None)
    return value


def _ensure_session() -> None:
    global _opener, _crumb, _session_at
    now = time.time()
    with _session_lock:
        if _opener is not None and now - _session_at < _SESSION_TTL:
            return
        jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
        for url in ("https://fc.yahoo.com", "https://finance.yahoo.com/"):
            try:
                opener.open(urllib.request.Request(url, headers=_UA), timeout=8)
            except Exception:
                continue
        crumb = ""
        for host in ("query1", "query2"):
            try:
                req = urllib.request.Request(f"https://{host}.finance.yahoo.com/v1/test/getcrumb", headers=_UA)
                with opener.open(req, timeout=8) as resp:
                    text = resp.read().decode("utf-8", "ignore").strip()
                if text and "<" not in text and "Too Many" not in text:
                    crumb = text
                    break
            except Exception:
                continue
        _opener = opener
        _crumb = crumb
        _session_at = now


def _throttle() -> None:
    global _last_request
    with _rate_lock:
        wait = _MIN_GAP - (time.time() - _last_request)
        if wait > 0:
            time.sleep(wait)
        _last_request = time.time()


def _with_crumb(url: str) -> str:
    if not _crumb or "crumb=" in url:
        return url
    join = "&" if "?" in url else "?"
    return f"{url}{join}crumb={urllib.parse.quote(_crumb)}"


def _host_variants(url: str) -> list[str]:
    if "query1.finance.yahoo.com" in url:
        return [url, url.replace("query1.finance.yahoo.com", "query2.finance.yahoo.com")]
    if "query2.finance.yahoo.com" in url:
        return [url, url.replace("query2.finance.yahoo.com", "query1.finance.yahoo.com")]
    return [url]


def _get_json(url: str) -> dict[str, Any]:
    _ensure_session()
    last_error: Exception | None = None
    for candidate in _host_variants(url):
        target = _with_crumb(candidate)
        for attempt in range(2):
            _throttle()
            req = urllib.request.Request(target, headers=_UA)
            try:
                opener = _opener or urllib.request.build_opener()
                with opener.open(req, timeout=12) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                last_error = exc
                if exc.code == 429 and attempt == 0:
                    time.sleep(1.6)
                    continue
                break
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                break
    if last_error:
        raise last_error
    raise RuntimeError("Yahoo request failed")


def yahoo_quote(symbols: list[str], deep: bool = True) -> list[dict[str, Any]]:
    if not symbols:
        return []
    try:
        chunk = ",".join(symbols[:40])
        url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=" + urllib.parse.quote(chunk)
        data = _get_json(url)
        results = (((data.get("quoteResponse") or {}).get("result")) or [])
        if results:
            rows = []
            for item in results:
                rows.append(
                    {
                        "symbol": item.get("symbol"),
                        "name": item.get("shortName") or item.get("longName") or item.get("symbol"),
                        "last": item.get("regularMarketPrice"),
                        "change": item.get("regularMarketChange"),
                        "percentage": item.get("regularMarketChangePercent"),
                        "volume": item.get("regularMarketVolume"),
                        "market_cap": item.get("marketCap") or 0,
                        "venue": _guess_venue(item.get("symbol")),
                    }
                )
            return rows
    except Exception:
        pass
    if not deep:
        return []
    from concurrent.futures import ThreadPoolExecutor

    def one(symbol: str) -> dict[str, Any] | None:
        try:
            candles = yahoo_ohlcv(symbol, "1d", 8)
            if not candles:
                return None
            last = candles[-1][4]
            prev = candles[-2][4] if len(candles) > 1 else last
            pct = ((last - prev) / prev * 100) if prev else 0.0
            return {
                "symbol": symbol,
                "name": symbol,
                "last": last,
                "percentage": pct,
                "volume": candles[-1][5],
                "market_cap": last * candles[-1][5],
                "venue": _guess_venue(symbol),
            }
        except Exception:
            return None

    with ThreadPoolExecutor(max_workers=8) as pool:
        return [row for row in pool.map(one, symbols[:40]) if row]


def yahoo_screener(scr_id: str, region: str = "US", count: int = 25) -> list[dict[str, Any]]:
    url = (
        "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"
        f"?formatted=false&scrIds={urllib.parse.quote(scr_id)}&count={count}&region={region}"
    )
    data = _get_json(url)
    quotes = ((((data.get("finance") or {}).get("result") or [{}])[0]).get("quotes")) or []
    rows = []
    for item in quotes:
        rows.append(
            {
                "symbol": item.get("symbol"),
                "name": item.get("shortName") or item.get("longName") or item.get("symbol"),
                "last": item.get("regularMarketPrice"),
                "percentage": item.get("regularMarketChangePercent"),
                "volume": item.get("regularMarketVolume"),
                "market_cap": item.get("marketCap") or 0,
                "venue": _guess_venue(item.get("symbol")),
            }
        )
    return rows


def yahoo_search(query: str) -> list[dict[str, Any]]:
    url = "https://query1.finance.yahoo.com/v1/finance/search?quotesCount=12&newsCount=0&q=" + urllib.parse.quote(
        query
    )
    data = _get_json(url)
    out = []
    for item in data.get("quotes") or []:
        symbol = item.get("symbol") or ""
        venue = _guess_venue(symbol)
        if venue == "us" and item.get("quoteType") in {"CRYPTOCURRENCY", "CURRENCY"}:
            venue = "crypto"
        out.append({"symbol": symbol, "name": item.get("shortname") or item.get("longname") or symbol, "venue": venue})
    return out


def yahoo_ohlcv(symbol: str, timeframe: str, limit: int = 300) -> list[list[Any]]:
    mapping = {
        "1s": ("1m", "1d"),
        "1m": ("1m", "5d"),
        "3m": ("5m", "5d"),
        "5m": ("5m", "5d"),
        "15m": ("15m", "1mo"),
        "30m": ("30m", "1mo"),
        "1h": ("60m", "3mo"),
        "2h": ("60m", "3mo"),
        "4h": ("60m", "6mo"),
        "6h": ("1d", "1y"),
        "12h": ("1d", "1y"),
        "1d": ("1d", "2y"),
        "3d": ("1d", "5y"),
        "1w": ("1wk", "10y"),
        "1M": ("1mo", "10y"),
        "1Y": ("1mo", "10y"),
    }
    interval, range_ = mapping.get(timeframe, ("1d", "1y"))
    url = (
        "https://query1.finance.yahoo.com/v8/finance/chart/"
        + urllib.parse.quote(symbol)
        + f"?interval={interval}&range={range_}"
    )
    data = _get_json(url)
    result = ((data.get("chart") or {}).get("result") or [None])[0]
    if not result:
        raise RuntimeError(f"No Yahoo chart data for {symbol}")
    ts = result.get("timestamp") or []
    quote = ((result.get("indicators") or {}).get("quote") or [{}])[0]
    rows = []
    for i, tstamp in enumerate(ts):
        o, h, l, c = quote["open"][i], quote["high"][i], quote["low"][i], quote["close"][i]
        v = (quote.get("volume") or [0] * len(ts))[i]
        if None in (o, h, l, c):
            continue
        rows.append([int(tstamp) * 1000, float(o), float(h), float(l), float(c), float(v or 0)])
    return rows[-limit:]


def rank_rows(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    valid = [r for r in rows if r.get("last") is not None]
    pool = valid or list(rows)
    gainers = sorted(pool, key=lambda r: r.get("percentage") or -999, reverse=True)[:20]
    losers = sorted(pool, key=lambda r: r.get("percentage") or 999)[:20]
    mcap = sorted(pool, key=lambda r: r.get("market_cap") or r.get("quote_volume") or 0, reverse=True)[:20]
    active = sorted(pool, key=lambda r: r.get("quote_volume") or r.get("volume") or 0, reverse=True)[:20]
    return {"gainers": gainers, "losers": losers, "mcap": mcap, "active": active}
