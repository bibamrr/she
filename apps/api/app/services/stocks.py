"""Equity data layer for the US and Saudi (Tadawul) desks.

Quotes and universes come from the public TradingView screener feed; candles come
from Twelve Data when ``SHC_TWELVEDATA_KEY`` is configured, otherwise from the
Yahoo chart endpoint that the crypto-free desks already used.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from apps.api.app.config import get_settings
from apps.api.app.services.tvfeed import tv_ohlcv
from apps.api.app.services.yahoo import _cached, rank_rows, yahoo_ohlcv

_CANDLE_DIR = Path("data/candles")
_FRESH_TTL = {
    "1d": 12 * 60,
    "3d": 20 * 60,
    "1w": 30 * 60,
    "1M": 45 * 60,
    "1Y": 45 * 60,
    "1h": 180,
    "2h": 180,
    "4h": 180,
    "6h": 300,
    "12h": 300,
}

_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
_SCANNER = "https://scanner.tradingview.com/{market}/scan"
_TWELVE = "https://api.twelvedata.com/time_series"

VENUES = {
    "us": {"market": "america", "suffix": ""},
    "tadawul": {"market": "ksa", "suffix": ".SR"},
    "europe": {"market": "uk", "suffix": ".L"},
    "asia": {"market": "japan", "suffix": ".T"},
    "commodities": {"market": "america", "suffix": ""},
}

EXCHANGE_YAHOO = {
    "LSE": ".L",
    "XETR": ".DE",
    "FWB": ".DE",
    "EURONEXT": ".PA",
    "SIX": ".SW",
    "BME": ".MC",
    "MIL": ".MI",
    "TSE": ".T",
    "JPX": ".T",
    "HKEX": ".HK",
    "KRX": ".KS",
    "SSE": ".SS",
    "SZSE": ".SZ",
    "ASX": ".AX",
    "NSE": ".NS",
    "BSE": ".BO",
    "TPE": ".TW",
}

REGION_MARKETS = {
    "europe": ["uk", "germany", "france"],
    "asia": ["japan", "hongkong"],
}

COMMODITIES = [
    {"symbol": "GC=F", "name": "Gold", "tv_symbol": "COMEX:GC1!", "sector": "Metals"},
    {"symbol": "SI=F", "name": "Silver", "tv_symbol": "COMEX:SI1!", "sector": "Metals"},
    {"symbol": "PL=F", "name": "Platinum", "tv_symbol": "NYMEX:PL1!", "sector": "Metals"},
    {"symbol": "HG=F", "name": "Copper", "tv_symbol": "COMEX:HG1!", "sector": "Metals"},
    {"symbol": "CL=F", "name": "WTI Crude", "tv_symbol": "NYMEX:CL1!", "sector": "Energy"},
    {"symbol": "BZ=F", "name": "Brent Crude", "tv_symbol": "NYMEX:BZ1!", "sector": "Energy"},
    {"symbol": "NG=F", "name": "Natural Gas", "tv_symbol": "NYMEX:NG1!", "sector": "Energy"},
    {"symbol": "RB=F", "name": "RBOB Gasoline", "tv_symbol": "NYMEX:RB1!", "sector": "Energy"},
    {"symbol": "HO=F", "name": "Heating Oil", "tv_symbol": "NYMEX:HO1!", "sector": "Energy"},
    {"symbol": "ZW=F", "name": "Wheat", "tv_symbol": "CBOT:ZW1!", "sector": "Agriculture"},
    {"symbol": "ZC=F", "name": "Corn", "tv_symbol": "CBOT:ZC1!", "sector": "Agriculture"},
    {"symbol": "ZS=F", "name": "Soybeans", "tv_symbol": "CBOT:ZS1!", "sector": "Agriculture"},
    {"symbol": "KC=F", "name": "Coffee", "tv_symbol": "ICEUS:KC1!", "sector": "Agriculture"},
    {"symbol": "CT=F", "name": "Cotton", "tv_symbol": "ICEUS:CT1!", "sector": "Agriculture"},
    {"symbol": "SB=F", "name": "Sugar", "tv_symbol": "ICEUS:SB1!", "sector": "Agriculture"},
]

EUROPE_SEED = [
    ("ASML.AS", "ASML"), ("MC.PA", "LVMH"), ("OR.PA", "L'Oréal"), ("AIR.PA", "Airbus"),
    ("SAP.DE", "SAP"), ("SIE.DE", "Siemens"), ("NESN.SW", "Nestlé"), ("NOVN.SW", "Novartis"),
    ("ROG.SW", "Roche"), ("SHEL.L", "Shell"), ("AZN.L", "AstraZeneca"), ("ULVR.L", "Unilever"),
    ("HSBA.L", "HSBC"), ("BP.L", "BP"), ("SAN.MC", "Santander"), ("ITX.MC", "Inditex"),
    ("ENEL.MI", "Enel"), ("ISP.MI", "Intesa"),
]

ASIA_SEED = [
    ("7203.T", "Toyota"), ("6758.T", "Sony"), ("9984.T", "SoftBank"), ("6861.T", "Keyence"),
    ("0700.HK", "Tencent"), ("9988.HK", "Alibaba"), ("3690.HK", "Meituan"),
    ("005930.KS", "Samsung"), ("000660.KS", "SK Hynix"), ("2330.TW", "TSMC"),
    ("INFY.NS", "Infosys"), ("RELIANCE.NS", "Reliance"), ("BHP.AX", "BHP"),
]

_COLUMNS = ["name", "description", "close", "change", "volume", "market_cap_basic", "sector"]

_TD_INTERVAL = {
    "1m": "1min",
    "3m": "5min",
    "5m": "5min",
    "15m": "15min",
    "30m": "30min",
    "1h": "1h",
    "2h": "2h",
    "4h": "4h",
    "6h": "4h",
    "12h": "1day",
    "1d": "1day",
    "3d": "1week",
    "1w": "1week",
    "1M": "1month",
}


def _post_json(url: str, payload: dict[str, Any], timeout: int = 20) -> dict[str, Any]:
    body = json.dumps(payload).encode()
    request = urllib.request.Request(
        url,
        data=body,
        headers={"User-Agent": _UA, "Content-Type": "application/json", "Accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode())


def _get_json(url: str, timeout: int = 20) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": _UA, "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode())


def venue_of(symbol: str) -> str:
    """Route a raw symbol to its desk: Saudi tickers are numeric or end with .SR."""
    clean = (symbol or "").upper().strip()
    if "/" in clean:
        return "crypto"
    if clean.endswith("=F") or clean.startswith("COMEX:") or clean.startswith("NYMEX:") or clean.startswith("CBOT:"):
        return "commodities"
    if clean.endswith(".SR") or clean.startswith("TADAWUL:") or clean.replace(".SR", "").isdigit():
        return "tadawul"
    if re.search(r"\.(L|PA|DE|AS|MI|SW|MC)$", clean):
        return "europe"
    if re.search(r"\.(T|HK|KS|KQ|SS|SZ|AX|TW|NS|BO)$", clean):
        return "asia"
    return "us"


def app_symbol(tv_symbol: str, venue: str) -> str:
    raw = tv_symbol or ""
    if ":" in raw:
        exch, ticker = raw.split(":", 1)
        suffix = EXCHANGE_YAHOO.get(exch)
        if suffix is not None:
            return f"{ticker}{suffix}"
        ticker_only = ticker
    else:
        ticker_only = raw
    return f"{ticker_only}{VENUES.get(venue, {}).get('suffix', '')}"


def _ticker_only(symbol: str) -> str:
    return symbol.upper().replace(".SR", "").replace("TADAWUL:", "").split(":")[-1]


def _scan_market(market: str, venue: str, limit: int) -> list[dict[str, Any]]:
    payload = {
        "filter": [{"left": "type", "operation": "equal", "right": "stock"}],
        "columns": _COLUMNS,
        "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"},
        "range": [0, limit],
    }
    data = _post_json(_SCANNER.format(market=market), payload)
    rows: list[dict[str, Any]] = []
    for item in data.get("data", []):
        values = item.get("d") or []
        if len(values) < 6:
            continue
        name, description, close, change, volume, mcap = values[:6]
        sector = values[6] if len(values) > 6 else ""
        rows.append(
            {
                "symbol": app_symbol(item.get("s", name), venue),
                "name": description or name,
                "last": close,
                "percentage": change,
                "volume": volume,
                "market_cap": mcap,
                "venue": venue,
                "sector": sector or "",
                "tv_symbol": item.get("s"),
            }
        )
    return rows


def _seed_universe(venue: str, seeds: list[tuple[str, str]]) -> list[dict[str, Any]]:
    from apps.api.app.services.yahoo import yahoo_quote

    quotes = {row["symbol"]: row for row in yahoo_quote([item[0] for item in seeds], deep=False)}
    rows: list[dict[str, Any]] = []
    for symbol, name in seeds:
        hit = quotes.get(symbol) or {}
        rows.append(
            {
                "symbol": symbol,
                "name": hit.get("name") or name,
                "last": hit.get("last"),
                "percentage": hit.get("percentage"),
                "volume": hit.get("volume"),
                "market_cap": hit.get("market_cap") or 0,
                "venue": venue,
                "sector": "",
            }
        )
    return rows


def commodity_universe() -> list[dict[str, Any]]:
    def load() -> list[dict[str, Any]]:
        from apps.api.app.services.yahoo import yahoo_quote

        quotes = {row["symbol"]: row for row in yahoo_quote([item["symbol"] for item in COMMODITIES], deep=False)}
        rows: list[dict[str, Any]] = []
        for spec in COMMODITIES:
            hit = quotes.get(spec["symbol"]) or {}
            rows.append(
                {
                    "symbol": spec["symbol"],
                    "name": hit.get("name") or spec["name"],
                    "last": hit.get("last"),
                    "percentage": hit.get("percentage"),
                    "volume": hit.get("volume"),
                    "market_cap": hit.get("market_cap") or 0,
                    "venue": "commodities",
                    "sector": spec["sector"],
                    "tv_symbol": spec["tv_symbol"],
                }
            )
        return rows

    return _cached("commodity_universe", 90, load)


def universe(venue: str, limit: int = 600) -> list[dict[str, Any]]:
    """Full tradable list for a venue, sorted by market cap."""
    if venue not in VENUES:
        raise ValueError(f"Unknown venue {venue}")
    if venue == "commodities":
        return commodity_universe()
    if venue in REGION_MARKETS:
        def load_region() -> list[dict[str, Any]]:
            merged: list[dict[str, Any]] = []
            seen: set[str] = set()
            per = max(40, limit // len(REGION_MARKETS[venue]))
            for market in REGION_MARKETS[venue]:
                try:
                    for row in _scan_market(market, venue, per):
                        if row["symbol"] in seen:
                            continue
                        seen.add(row["symbol"])
                        merged.append(row)
                except Exception:
                    continue
            if not merged:
                seeds = EUROPE_SEED if venue == "europe" else ASIA_SEED
                return _seed_universe(venue, seeds)
            merged.sort(key=lambda item: float(item.get("market_cap") or 0), reverse=True)
            return merged[:limit]

        return _cached(f"stock_universe:{venue}:{limit}", 90, load_region)

    def load() -> list[dict[str, Any]]:
        return _scan_market(VENUES[venue]["market"], venue, limit)

    return _cached(f"stock_universe:{venue}:{limit}", 90, load)


def scan(venue: str) -> dict[str, Any]:
    rows = universe(venue)
    ranked = rank_rows(rows)
    ranked["venue"] = venue
    ranked["all_count"] = len(rows)
    ranked["sectors"] = sector_groups(rows)
    if not rows:
        ranked["warning"] = "upstream screener unavailable"
    return ranked


def sector_groups(rows: list[dict[str, Any]], limit: int = 12) -> list[dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        name = (row.get("sector") or "").strip() or "Other"
        buckets.setdefault(name, []).append(row)
    ranked: list[dict[str, Any]] = []
    for name, items in buckets.items():
        if name == "Other" and len(buckets) > 1:
            continue
        pcts = [float(item.get("percentage") or 0) for item in items]
        avg = sum(pcts) / len(pcts) if pcts else 0.0
        leader = max(items, key=lambda item: abs(float(item.get("percentage") or 0)))
        ranked.append(
            {
                "sector": name,
                "count": len(items),
                "percentage": round(avg, 2),
                "leader": leader.get("symbol"),
                "leader_name": leader.get("name"),
                "venue": leader.get("venue"),
            }
        )
    ranked.sort(key=lambda item: item["percentage"], reverse=True)
    return ranked[:limit]


INDEX_SPECS = [
    {"id": "tasi", "tv": "TADAWUL:TASI", "yahoo": "^TASI", "label_ar": "تاسي", "label_en": "TASI", "venue": "tadawul"},
    {"id": "spx", "tv": "SP:SPX", "yahoo": "^GSPC", "label_ar": "S&P 500", "label_en": "S&P 500", "venue": "us"},
    {"id": "ixic", "tv": "NASDAQ:IXIC", "yahoo": "^IXIC", "label_ar": "ناسداك", "label_en": "NASDAQ", "venue": "us"},
    {"id": "dax", "tv": "XETR:DAX", "yahoo": "^GDAXI", "label_ar": "داكس", "label_en": "DAX", "venue": "europe"},
    {"id": "ukx", "tv": "LSE:UKX", "yahoo": "^FTSE", "label_ar": "فوتسي", "label_en": "FTSE 100", "venue": "europe"},
    {"id": "nky", "tv": "TSE:NI225", "yahoo": "^N225", "label_ar": "نيكي", "label_en": "Nikkei 225", "venue": "asia"},
    {"id": "hsi", "tv": "HKEX:HSI", "yahoo": "^HSI", "label_ar": "هانغ سنغ", "label_en": "Hang Seng", "venue": "asia"},
    {"id": "gold", "tv": "TVC:GOLD", "yahoo": "GC=F", "label_ar": "الذهب", "label_en": "Gold", "venue": "commodities"},
]


def fetch_indices() -> list[dict[str, Any]]:
    def load() -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        try:
            payload = {
                "symbols": {"tickers": [spec["tv"] for spec in INDEX_SPECS]},
                "columns": ["name", "description", "close", "change", "change_abs", "volume"],
            }
            data = _post_json("https://scanner.tradingview.com/global/scan", payload, timeout=12)
            by_tv = {item.get("s"): item.get("d") or [] for item in data.get("data", [])}
            for spec in INDEX_SPECS:
                values = by_tv.get(spec["tv"]) or []
                if len(values) < 4:
                    continue
                rows.append(
                    {
                        "id": spec["id"],
                        "symbol": spec["tv"],
                        "name_ar": spec["label_ar"],
                        "name_en": spec["label_en"],
                        "last": values[2],
                        "percentage": values[3],
                        "venue": spec["venue"],
                        "source": "tradingview",
                    }
                )
        except Exception:
            rows = []
        if len(rows) < 3:
            try:
                from apps.api.app.services.yahoo import yahoo_quote

                ysymbols = [spec["yahoo"] for spec in INDEX_SPECS] + ["^TASI.SR"]
                quotes = {item.get("symbol"): item for item in yahoo_quote(ysymbols)}
                if "^TASI.SR" in quotes and "^TASI" not in quotes:
                    quotes["^TASI"] = quotes["^TASI.SR"]
                for spec in INDEX_SPECS:
                    if any(row["id"] == spec["id"] for row in rows):
                        continue
                    quote = quotes.get(spec["yahoo"])
                    if not quote:
                        continue
                    rows.append(
                        {
                            "id": spec["id"],
                            "symbol": spec["yahoo"],
                            "name_ar": spec["label_ar"],
                            "name_en": spec["label_en"],
                            "last": quote.get("last"),
                            "percentage": quote.get("percentage"),
                            "venue": spec["venue"],
                            "source": "yahoo",
                        }
                    )
            except Exception:
                pass
        return rows

    return _cached("market_indices", 45, load)


def stock_fundamentals(symbol: str) -> dict[str, Any] | None:
    """One-symbol fundamentals; isolated from the universe scan so PE never breaks lists."""
    row = quote(symbol)
    if not row:
        return None
    tv = row.get("tv_symbol")
    if not tv:
        return {**row, "pe": None, "industry": ""}

    def load() -> dict[str, Any]:
        extra = dict(row)
        try:
            market = VENUES[venue_of(symbol)]["market"]
            payload = {
                "symbols": {"tickers": [tv]},
                "columns": [
                    "name",
                    "description",
                    "close",
                    "change",
                    "volume",
                    "market_cap_basic",
                    "price_earnings_ttm",
                    "sector",
                    "industry",
                    "total_shares_outstanding",
                    "float_shares_outstanding",
                    "average_volume_30d_calc",
                ],
            }
            data = _post_json(_SCANNER.format(market=market), payload, timeout=12)
            values = ((data.get("data") or [{}])[0].get("d")) or []
            if len(values) >= 7:
                extra["pe"] = values[6]
            if len(values) >= 8:
                extra["sector"] = values[7] or extra.get("sector")
            if len(values) >= 9:
                extra["industry"] = values[8] or ""
            if len(values) >= 10:
                extra["shares_outstanding"] = values[9]
            if len(values) >= 11:
                extra["shares_float"] = values[10]
            if len(values) >= 12:
                extra["avg_volume"] = values[11]
        except Exception:
            extra.setdefault("pe", None)
            extra.setdefault("industry", "")
        return extra

    return _cached(f"fundamentals:{symbol}", 180, load)


def quote(symbol: str) -> dict[str, Any] | None:
    venue = venue_of(symbol)
    ticker = _ticker_only(symbol)
    for row in universe(venue):
        if _ticker_only(row["symbol"]) == ticker:
            return row
    return None


def search(query: str, limit: int = 12) -> list[dict[str, Any]]:
    needle = query.strip().upper()
    if not needle:
        return []
    hits: list[dict[str, Any]] = []
    for venue in ("tadawul", "us", "europe", "asia", "commodities"):
        try:
            rows = universe(venue)
        except Exception:
            continue
        for row in rows:
            haystack = f"{row['symbol']} {row['name']}".upper()
            if needle in haystack:
                hits.append(row)
            if len(hits) >= limit * 2:
                break
    hits.sort(key=lambda r: (not r["symbol"].upper().startswith(needle), -(r.get("market_cap") or 0)))
    return hits[:limit]


def _twelvedata_ohlcv(symbol: str, timeframe: str, limit: int) -> list[list[Any]]:
    key = get_settings().twelvedata_key
    interval = _TD_INTERVAL.get(timeframe, "1day")
    venue = venue_of(symbol)
    params = {
        "symbol": _ticker_only(symbol),
        "interval": interval,
        "outputsize": str(min(limit, 5000)),
        "apikey": key,
        "order": "ASC",
        "format": "JSON",
    }
    if venue == "tadawul":
        params["exchange"] = "Tadawul"
    query = urllib.parse.urlencode(params)
    data = _get_json(f"{_TWELVE}?{query}")
    if data.get("status") == "error":
        raise RuntimeError(data.get("message") or "twelvedata error")
    rows: list[list[Any]] = []
    for bar in data.get("values", []):
        stamp = bar["datetime"]
        fmt = "%Y-%m-%d %H:%M:%S" if len(stamp) > 10 else "%Y-%m-%d"
        ts = int(dt.datetime.strptime(stamp, fmt).replace(tzinfo=dt.timezone.utc).timestamp() * 1000)
        rows.append(
            [
                ts,
                float(bar["open"]),
                float(bar["high"]),
                float(bar["low"]),
                float(bar["close"]),
                float(bar.get("volume") or 0),
            ]
        )
    return rows[-limit:]


def _cache_path(symbol: str, timeframe: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", symbol.upper())
    return _CANDLE_DIR / f"{safe}_{timeframe}.json"


def _read_candle_cache(symbol: str, timeframe: str, max_age: float | None) -> list[list[Any]] | None:
    path = _cache_path(symbol, timeframe)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text())
    except Exception:
        return None
    stamp = float(payload.get("ts") or 0)
    if max_age is not None and time.time() - stamp > max_age:
        return None
    rows = payload.get("rows") or []
    return rows if rows else None


def _write_candle_cache(symbol: str, timeframe: str, rows: list[list[Any]]) -> None:
    if not rows:
        return
    try:
        _CANDLE_DIR.mkdir(parents=True, exist_ok=True)
        _cache_path(symbol, timeframe).write_text(json.dumps({"ts": time.time(), "rows": rows[-1500:]}))
    except Exception:
        pass


def _tv_symbol(symbol: str) -> str:
    row = quote(symbol)
    if row and row.get("tv_symbol"):
        return str(row["tv_symbol"])
    ticker = _ticker_only(symbol)
    venue = venue_of(symbol)
    if venue == "tadawul":
        return f"TADAWUL:{ticker}"
    if venue == "commodities":
        for spec in COMMODITIES:
            if spec["symbol"].upper() == symbol.upper():
                return spec["tv_symbol"]
    return ticker


def _quote_bar(symbol: str) -> list[Any] | None:
    return _cached(f"quote_bar:{symbol}", 45, lambda: _quote_bar_load(symbol))


def _quote_bar_load(symbol: str) -> list[Any] | None:
    row = quote(symbol)
    tv = _tv_symbol(symbol)
    values: list[Any] = []
    try:
        market = VENUES[venue_of(symbol)]["market"]
        data = _post_json(
            _SCANNER.format(market=market),
            {"symbols": {"tickers": [tv]}, "columns": ["open", "high", "low", "close", "volume"]},
            timeout=10,
        )
        values = ((data.get("data") or [{}])[0].get("d")) or []
    except Exception:
        values = []
    last = None
    if len(values) >= 4:
        try:
            open_, high, low, close = (float(values[0]), float(values[1]), float(values[2]), float(values[3]))
            volume = float(values[4] or 0) if len(values) > 4 else 0.0
            last = [open_, high, low, close, volume]
        except (TypeError, ValueError):
            last = None
    if last is None and row and row.get("last") is not None:
        px = float(row["last"])
        last = [px, px, px, px, float(row.get("volume") or 0)]
    if last is None:
        return None
    day = (int(time.time()) // 86400) * 86400 * 1000
    return [day, *last]


def _patch_last_bar(rows: list[list[Any]], symbol: str) -> list[list[Any]]:
    bar = _quote_bar(symbol)
    if not bar:
        return rows
    if not rows:
        return [bar]
    out = [list(item) for item in rows]
    prev = out[-1]
    # same session: morph the last printed bar; otherwise append today's quote bar
    if abs(int(prev[0]) - int(bar[0])) <= 86_400_000:
        prev[2] = max(float(prev[2]), float(bar[2]), float(bar[4]))
        prev[3] = min(float(prev[3]), float(bar[3]), float(bar[4]))
        prev[4] = float(bar[4])
        if bar[5]:
            prev[5] = float(bar[5])
    else:
        out.append(bar)
    return out


def stock_ohlcv(symbol: str, timeframe: str, limit: int = 300) -> list[list[Any]]:
    errors: list[str] = []
    fresh_for = _FRESH_TTL.get(timeframe, 75)

    def finish(rows: list[list[Any]], persist: bool = True) -> list[list[Any]]:
        patched = _patch_last_bar(rows, symbol)
        if persist:
            _write_candle_cache(symbol, timeframe, patched)
        return patched[-limit:]

    if get_settings().twelvedata_key:
        try:
            rows = _twelvedata_ohlcv(symbol, timeframe, limit)
            if rows:
                return finish(rows)
            errors.append("twelvedata returned no bars")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"twelvedata: {exc}")

    cached = _read_candle_cache(symbol, timeframe, fresh_for)
    if cached:
        return finish(cached, persist=False)

    try:
        rows = tv_ohlcv(_tv_symbol(symbol), timeframe, limit)
        if rows:
            return finish(rows)
        errors.append("tradingview returned no bars")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"tradingview: {exc}")

    try:
        rows = yahoo_ohlcv(symbol, timeframe, limit)
        if rows:
            return finish(rows)
        errors.append("yahoo returned no bars")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"yahoo: {exc}")

    stale = _read_candle_cache(symbol, timeframe, None)
    if stale:
        return finish(stale, persist=False)

    bar = _quote_bar(symbol)
    if bar:
        return finish([bar])

    raise RuntimeError(
        "No candle provider available for "
        f"{symbol} ({'; '.join(errors)}). Set SHC_TWELVEDATA_KEY for a dedicated equity feed."
    )


def provider_status() -> dict[str, Any]:
    settings = get_settings()
    status: dict[str, Any] = {
        "candles_provider": "twelvedata" if settings.twelvedata_key else "yahoo+tradingview",
        "twelvedata_configured": bool(settings.twelvedata_key),
        "venues": {},
    }
    for venue in VENUES:
        try:
            rows = universe(venue)
            status["venues"][venue] = {"ok": bool(rows), "symbols": len(rows)}
        except Exception as exc:  # noqa: BLE001
            status["venues"][venue] = {"ok": False, "error": str(exc)}
    return status
