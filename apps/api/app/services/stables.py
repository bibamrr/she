"""Stablecoin exclusion and dead-range volatility gates for the crypto hunter."""

from __future__ import annotations

from typing import Any, Optional

# Bases that peg to fiat / another stable without "USD" in the ticker.
_FIAT_STABLES = frozenset(
    {
        "DAI",
        "FRAX",
        "GHO",
        "MIM",
        "FEI",
        "DOLA",
        "PAX",
        "EURC",
        "EURT",
        "EURI",
        "AEUR",
        "EURS",
        "EURO",
        "EURCV",
        "XSGD",
        "IDRT",
        "BIDR",
        "TRYB",
        "BRZ",
        "CADC",
        "GYEN",
        "XIDR",
        "USR",
        "GUSD",
    }
)

_QUOTES = ("USDT", "USDC", "BUSD", "FDUSD", "TUSD", "DAI", "USD", "BTC", "ETH")

# ATR / 20-bar span must exceed the typical stablecoin dead band.
MIN_ATR_PCT = 0.0008
MIN_SPAN_PCT = 0.0025
PEG_LOW = 0.97
PEG_HIGH = 1.03
PEG_ATR_MAX = 0.003


def base_asset(symbol: str) -> str:
    raw = (symbol or "").strip().upper().split(":")[0]
    if "/" in raw:
        return raw.split("/")[0].replace(" ", "")
    compact = raw.replace("-", "").replace("_", "")
    for quote in _QUOTES:
        if compact.endswith(quote) and len(compact) > len(quote):
            return compact[: -len(quote)]
    return compact


def is_stablecoin(symbol: str) -> bool:
    """True when the traded asset itself is a dollar/fiat-pegged stable."""
    base = base_asset(symbol)
    if not base:
        return False
    if base in _FIAT_STABLES:
        return True
    if "USD" in base:
        return True
    return False


def is_pegged_quote(row: dict[str, Any]) -> bool:
    """Cheap ticker-level catch for unnamed $1 stables with almost no 24h move."""
    try:
        last = float(row.get("last") or 0)
        pct = abs(float(row.get("percentage") or 0))
    except (TypeError, ValueError):
        return False
    return PEG_LOW <= last <= PEG_HIGH and pct < 0.35


def skip_crypto_hunter(symbol: str, row: Optional[dict[str, Any]] = None) -> bool:
    if is_stablecoin(symbol):
        return True
    if row and is_pegged_quote(row):
        return True
    return False


def has_tradable_volatility(df: Any) -> bool:
    """Reject the flat band stables live in, even if the ticker name is new."""
    if df is None or len(df) < 20:
        return False
    try:
        close = float(df["close"].iloc[-1])
    except Exception:
        return False
    if close <= 0:
        return False
    try:
        from indicators.volatility import atr

        last_atr = float(atr(df, 14).iloc[-1] or 0)
    except Exception:
        last_atr = 0.0
    atr_pct = last_atr / close if last_atr > 0 else 0.0
    window = df.tail(20)
    span = float(window["high"].max() - window["low"].min())
    span_pct = span / close if span > 0 else 0.0
    if PEG_LOW <= close <= PEG_HIGH and atr_pct < PEG_ATR_MAX:
        return False
    return atr_pct >= MIN_ATR_PCT and span_pct >= MIN_SPAN_PCT
