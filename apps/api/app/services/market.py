from __future__ import annotations

import threading
from typing import Any, Callable, TypeVar

import ccxt

from apps.api.app.services import stocks
from apps.api.app.services.memory import clamp_limit, tail

_lock = threading.Lock()
_exchanges: dict[str, ccxt.Exchange] = {}
_blocked: set[str] = set()
_T = TypeVar("_T")

_GEO_HINTS = (
    "451",
    "403",
    "restricted location",
    "unavailable from a restricted",
    "eligibility",
    "restricted location according",
    "cloudfront",
    "not available in your region",
    "service not available in your area",
)
_SPOT_CHAIN = ("binance", "bybit", "okx", "kucoin")
_FUTURES_CHAIN = ("binance", "bybit", "okx", "kucoin")
_GEO_STATUSES = {403, 451}

_CRYPTO_QUOTES = ("USDT", "USDC", "BUSD", "FDUSD", "USD")
_FUTURES_MARKS = {"FUT", "P", "PERP", "USDT"}
_EXCHANGE_ALIASES = {
    "BINANCE": "binance",
    "BINANCEUSDM": "binance",
    "BINANCE-FUTURES": "binance",
}

WATCHLIST = [
    {"symbol": "BTC/USDT", "label": "Bitcoin"},
    {"symbol": "ETH/USDT", "label": "Ethereum"},
    {"symbol": "SOL/USDT", "label": "Solana"},
    {"symbol": "XRP/USDT", "label": "XRP"},
    {"symbol": "BNB/USDT", "label": "BNB"},
]

TIMEFRAMES = [
    {"id": "1s", "label": "1s"},
    {"id": "1m", "label": "1m"},
    {"id": "3m", "label": "3m"},
    {"id": "5m", "label": "5m"},
    {"id": "15m", "label": "15m"},
    {"id": "30m", "label": "30m"},
    {"id": "1h", "label": "1h"},
    {"id": "2h", "label": "2h"},
    {"id": "4h", "label": "4h"},
    {"id": "6h", "label": "6h"},
    {"id": "12h", "label": "12h"},
    {"id": "1d", "label": "1D"},
    {"id": "3d", "label": "3D"},
    {"id": "1w", "label": "1W"},
    {"id": "1M", "label": "1M"},
    {"id": "1Y", "label": "1Y"},
]

TF_SOURCE = {"1Y": "1M"}
TF_MS = {
    "1s": 1_000,
    "1m": 60_000,
    "3m": 180_000,
    "5m": 300_000,
    "15m": 900_000,
    "30m": 1_800_000,
    "1h": 3_600_000,
    "2h": 7_200_000,
    "4h": 14_400_000,
    "6h": 21_600_000,
    "12h": 43_200_000,
    "1d": 86_400_000,
}


def normalize_timeframe(timeframe: str) -> str:
    return TF_SOURCE.get(timeframe, timeframe)


def rows_to_candles(rows: list[list[Any]]) -> list[dict[str, Any]]:
    return [
        {"time": int(ts / 1000), "open": o, "high": h, "low": l, "close": c, "volume": v}
        for ts, o, h, l, c, v in rows
    ]


def sync_ohlcv(rows: list[list[Any]]) -> list[list[Any]]:
    """Deduplicate, sort and drop broken bars so live ticks align with history."""
    by_ts: dict[int, list[Any]] = {}
    for row in rows:
        if not row or len(row) < 6:
            continue
        ts = int(row[0])
        if ts <= 0:
            continue
        try:
            o, h, l, c, v = (float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5] or 0))
        except (TypeError, ValueError):
            continue
        if h < l or o <= 0 or c <= 0:
            continue
        high = max(h, o, c)
        low = min(l, o, c)
        by_ts[ts] = [ts, o, high, low, c, max(v, 0.0)]
    return [by_ts[ts] for ts in sorted(by_ts)]


def fill_crypto_gaps(rows: list[list[Any]], timeframe: str, max_fill: int = 3) -> list[list[Any]]:
    """Insert flat bars for 1–3 missing crypto intervals so live ticks stay aligned."""
    step = TF_MS.get(timeframe)
    if not step or len(rows) < 3:
        return rows
    out = [rows[0]]
    for row in rows[1:]:
        prev = out[-1]
        missing = int(round((row[0] - prev[0]) / step)) - 1
        if 1 <= missing <= max_fill:
            close = prev[4]
            for index in range(1, missing + 1):
                out.append([prev[0] + step * index, close, close, close, close, 0.0])
        out.append(row)
    return out


def delay_ohlcv(rows: list[list[Any]], drop_last: int = 3) -> list[list[Any]]:
    """Explorer equity feed: hide the most recent unfinished bars."""
    if len(rows) <= drop_last + 20:
        return rows[:-1] if len(rows) > 1 else rows
    return rows[:-drop_last]


def parse_market_symbol(symbol: str) -> dict[str, Any]:
    """Split a desk symbol into display pair, exchange, and spot/futures."""
    raw = (symbol or "").strip().upper().replace(" ", "")
    exchange = "binance"
    market_type = "spot"
    empty = {
        "desk": "",
        "ccxt": "",
        "display": "",
        "exchange": "",
        "market_type": "",
        "crypto": False,
    }
    if not raw:
        return empty
    if ":" in raw:
        left, right = raw.split(":", 1)
        if left in _EXCHANGE_ALIASES:
            exchange = _EXCHANGE_ALIASES[left]
            raw = right
            if left == "BINANCEUSDM":
                market_type = "futures"
    if ":" in raw:
        body, mark = raw.rsplit(":", 1)
        if mark in _FUTURES_MARKS:
            raw = body
            market_type = "futures"
    if "/" not in raw:
        for quote in _CRYPTO_QUOTES:
            if raw.endswith(quote) and len(raw) > len(quote):
                raw = f"{raw[: -len(quote)]}/{quote}"
                break
    display = raw
    if "/" not in display:
        original = (symbol or "").strip().upper()
        return {**empty, "desk": original, "display": original}
    desk = f"{display}:FUT" if market_type == "futures" else display
    ccxt_symbol = f"{display}:USDT" if market_type == "futures" else display
    return {
        "desk": desk,
        "ccxt": ccxt_symbol,
        "display": display,
        "exchange": exchange,
        "market_type": market_type,
        "crypto": True,
    }


def desk_symbol(symbol: str) -> str:
    spec = parse_market_symbol(symbol)
    return spec["desk"] or (symbol or "").strip().upper()


def _settings():
    from apps.api.app.config import get_settings

    return get_settings()


def _proxy_url() -> str:
    """Return a single HTTP(S) proxy URL, if the operator configured one."""
    return (_settings().market_http_proxy or "").strip()


def binance_rest_v3_base(host: str = "") -> str:
    """Public Binance REST root: https://data-api.binance.vision/api/v3."""
    raw = (host or _settings().binance_rest_host or "https://data-api.binance.vision").rstrip("/")
    if raw.endswith("/api/v3"):
        return raw
    return f"{raw}/api/v3"


def _binance_url_overrides(host: str) -> dict[str, str]:
    """ccxt already appends /exchangeInfo to `public`, so `public` must include /api/v3."""
    raw = (host or "https://data-api.binance.vision").rstrip("/")
    if raw.endswith("/api/v3"):
        root = raw[: -len("/api/v3")]
        public = raw
    else:
        root = raw
        public = f"{raw}/api/v3"
    return {
        "public": public,
        "private": public,
        "v1": f"{root}/api/v1",
    }


def _is_geo_blocked(exc: BaseException) -> bool:
    status = getattr(exc, "http_status", None) or getattr(exc, "status", None)
    if status in _GEO_STATUSES:
        return True
    text = str(exc).lower()
    return any(hint in text for hint in _GEO_HINTS)


def _venue_chain(market_type: str) -> tuple[str, ...]:
    if market_type == "futures":
        if _proxy_url():
            return _FUTURES_CHAIN
        # fapi.binance.com is geo-blocked from US clouds; skip unless a proxy is set.
        # Bybit public REST often returns 403 from the same regions — OKX/KuCoin stay reachable.
        return ("okx", "kucoin", "bybit")
    return _SPOT_CHAIN


def _okx_inst_id(spec: dict[str, Any]) -> str:
    """OKX native ids use dashes: BTC-USDT spot, BTC-USDT-SWAP perpetual."""
    display = spec.get("display") or ""
    inst = display.replace("/", "-")
    if spec.get("market_type") == "futures":
        if not inst.endswith("-SWAP"):
            inst = f"{inst}-SWAP"
        return inst
    return inst


def _venue_symbol(name: str, spec: dict[str, Any]) -> str:
    if name == "okx":
        return _okx_inst_id(spec)
    if name == "binance":
        return spec["ccxt"]
    if spec["market_type"] == "futures":
        return f"{spec['display']}:USDT"
    return spec["display"]


def _timeframe_for(name: str, timeframe: str) -> str:
    if timeframe == "1s" and name != "binance":
        return "1m"
    return timeframe


def _make_client(name: str, market_type: str) -> ccxt.Exchange:
    kind = "futures" if market_type == "futures" else "spot"
    proxy = _proxy_url()
    options: dict[str, Any] = {
        "enableRateLimit": True,
        "timeout": 20_000,
        "headers": {"User-Agent": "Mozilla/5.0 (compatible; SHC-market/1.0)"},
        "options": {
            "adjustForTimeDifference": True,
            "fetchCurrencies": False,
        },
    }
    if name == "binance":
        host = (_settings().binance_rest_host or "https://data-api.binance.vision").rstrip("/")
        factory = ccxt.binanceusdm if kind == "futures" else ccxt.binance
        if kind == "spot":
            options["urls"] = {"api": _binance_url_overrides(host)}
            options["options"]["defaultType"] = "spot"
        else:
            options["options"]["defaultType"] = "future"
        client = factory(options)
        # Prevent sapi calls to api.binance.com (those still return 451 from US clouds).
        client.has["fetchCurrencies"] = False
    elif name == "bybit":
        options["options"]["defaultType"] = "linear" if kind == "futures" else "spot"
        client = ccxt.bybit(options)
    elif name == "okx":
        options["options"]["defaultType"] = "swap" if kind == "futures" else "spot"
        client = ccxt.okx(options)
    elif name == "kucoin":
        options["options"]["defaultType"] = "swap" if kind == "futures" else "spot"
        factory = ccxt.kucoinfutures if kind == "futures" else ccxt.kucoin
        client = factory(options)
        client.has["fetchCurrencies"] = False
    else:
        raise ValueError(f"Unsupported crypto venue: {name}")
    client.httpProxy = None
    client.httpsProxy = proxy or None
    return client


def _client(name: str, market_type: str) -> ccxt.Exchange:
    key = f"{name}:{market_type}"
    with _lock:
        cached = _exchanges.get(key)
        if cached is None:
            cached = _make_client(name, market_type)
            _exchanges[key] = cached
        return cached


def _mark_blocked(name: str, exc: BaseException) -> None:
    if _is_geo_blocked(exc):
        _blocked.add(name)


def _try_venues(market_type: str, runner: Callable[[ccxt.Exchange, str], _T]) -> _T:
    errors: list[str] = []
    for name in _venue_chain(market_type):
        if name in _blocked:
            continue
        try:
            return runner(_client(name, market_type), name)
        except Exception as exc:  # noqa: BLE001
            _mark_blocked(name, exc)
            errors.append(f"{name}: {exc}")
    raise RuntimeError("No reachable crypto market-data venue: " + "; ".join(errors))


def get_exchange(market_type: str = "spot") -> ccxt.Exchange:
    kind = "futures" if str(market_type or "").lower() == "futures" else "spot"
    last_exc: Exception | None = None
    for name in _venue_chain(kind):
        if name in _blocked:
            continue
        try:
            return _client(name, kind)
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            _mark_blocked(name, exc)
    if last_exc:
        raise last_exc
    fallback = next((name for name in _venue_chain(kind) if name not in _blocked), "okx")
    return _client(fallback, kind)


def fetch_crypto_tickers(market_type: str = "spot") -> dict[str, Any]:
    kind = "futures" if str(market_type or "").lower() == "futures" else "spot"
    return _try_venues(kind, lambda client, _name: client.fetch_tickers())


def is_crypto(symbol: str) -> bool:
    return bool(parse_market_symbol(symbol)["crypto"]) or "/" in (symbol or "")


def fetch_ohlcv(symbol: str, timeframe: str, limit: int = 300, delayed: bool = False) -> list[list[Any]]:
    tf = normalize_timeframe(timeframe)
    limit = clamp_limit(limit)
    extra = 8 if delayed else 0
    spec = parse_market_symbol(symbol)
    if not spec["crypto"]:
        rows = stocks.stock_ohlcv(symbol, tf, limit + extra)
        synced = sync_ohlcv(rows)
        synced = delay_ohlcv(synced) if delayed else synced
        return tail(synced, limit)

    def load(client: ccxt.Exchange, name: str) -> list[list[Any]]:
        used = _timeframe_for(name, tf)

        def pull(pair: str, timeframe: str) -> list[list[Any]]:
            return client.fetch_ohlcv(pair, timeframe=timeframe, limit=limit + extra)

        pair = _venue_symbol(name, spec)
        try:
            return pull(pair, used)
        except Exception:
            alt = spec["ccxt"] if spec["market_type"] == "futures" else spec["display"]
            if name == "okx" and alt != pair:
                try:
                    return pull(alt, used)
                except Exception:
                    pass
            if used == "1s":
                return pull(pair, "1m")
            raise

    rows = _try_venues(spec["market_type"], load)
    synced = fill_crypto_gaps(sync_ohlcv(rows), tf)
    if delayed and not spec["crypto"]:
        synced = delay_ohlcv(synced, 1)
    return tail(synced, limit)


def fetch_ticker(symbol: str) -> dict[str, Any]:
    spec = parse_market_symbol(symbol)
    if not spec["crypto"]:
        row = stocks.quote(symbol)
        if not row:
            raise RuntimeError(f"No quote for {symbol}")
        return {
            "last": row.get("last"),
            "percentage": row.get("percentage"),
            "bid": row.get("last"),
            "ask": row.get("last"),
            "high": None,
            "low": None,
            "baseVolume": row.get("volume"),
            "venue": row.get("venue"),
            "name": row.get("name"),
        }
    def load_ticker(client: ccxt.Exchange, name: str) -> dict[str, Any]:
        pair = _venue_symbol(name, spec)
        try:
            return client.fetch_ticker(pair)
        except Exception:
            alt = spec["ccxt"] if spec["market_type"] == "futures" else spec["display"]
            if name == "okx" and alt != pair:
                return client.fetch_ticker(alt)
            raise

    data = _try_venues(spec["market_type"], load_ticker)
    data["exchange"] = spec["exchange"]
    data["market_type"] = spec["market_type"]
    data["display_symbol"] = spec["display"]
    data["symbol"] = spec["desk"]
    return data


def fetch_order_book(symbol: str, limit: int = 50) -> dict[str, Any]:
    spec = parse_market_symbol(symbol)
    if not spec["crypto"]:
        return get_exchange().fetch_order_book(symbol, limit=limit)
    def load_book(client: ccxt.Exchange, name: str) -> dict[str, Any]:
        pair = _venue_symbol(name, spec)
        try:
            return client.fetch_order_book(pair, limit=limit)
        except Exception:
            alt = spec["ccxt"] if spec["market_type"] == "futures" else spec["display"]
            if name == "okx" and alt != pair:
                return client.fetch_order_book(alt, limit=limit)
            raise

    return _try_venues(spec["market_type"], load_book)
