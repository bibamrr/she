"""Isolated fundamentals + liquidity sentiment — never sits on the candle tick path."""

from __future__ import annotations

import json
import urllib.request
from typing import Any

import pandas as pd

from apps.api.app.services import stocks
from apps.api.app.services.market import fetch_ohlcv, is_crypto
from apps.api.app.services.yahoo import _cached, _get_json
from indicators.momentum import rsi


def _sentiment_from_bars(rows: list[list[Any]]) -> dict[str, Any]:
    sample = rows[-36:] if len(rows) > 36 else rows
    if len(sample) < 8:
        return {"score": 50, "bias": "neutral", "buy_volume": 0, "sell_volume": 0}
    buy = 0.0
    sell = 0.0
    for _ts, open_, _h, _l, close, volume in sample:
        vol = float(volume or 0)
        if close >= open_:
            buy += vol
        else:
            sell += vol
    total = buy + sell
    ratio = ((buy - sell) / total) if total else 0.0
    score = max(0.0, min(100.0, round(50 + ratio * 50, 1)))
    if score >= 62:
        bias = "risk_on"
    elif score <= 38:
        bias = "risk_off"
    else:
        bias = "neutral"
    return {
        "score": score,
        "bias": bias,
        "buy_volume": round(buy, 2),
        "sell_volume": round(sell, 2),
    }


def sentiment(symbol: str, timeframe: str = "1h") -> dict[str, Any]:
    def load() -> dict[str, Any]:
        rows = fetch_ohlcv(symbol, timeframe, 80)
        payload = _sentiment_from_bars(rows)
        payload["symbol"] = symbol
        payload["timeframe"] = timeframe
        payload["venue"] = "crypto" if is_crypto(symbol) else stocks.venue_of(symbol)
        return payload

    return _cached(f"sentiment:{symbol}:{timeframe}", 45, load)


def _crypto_base(symbol: str) -> str:
    return (symbol.split("/")[0] if "/" in symbol else symbol).split("-")[0].upper()


def _public_json(url: str) -> Any:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 SHC/1.0", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _crypto_meta(symbol: str) -> dict[str, Any]:
    base = _crypto_base(symbol).lower()
    if not base:
        return {}

    def load() -> dict[str, Any]:
        try:
            url = (
                "https://api.coingecko.com/api/v3/coins/markets"
                f"?vs_currency=usd&symbols={base}&order=market_cap_desc&per_page=8&sparkline=false"
            )
            rows = _public_json(url)
        except Exception:
            rows = []
        if not isinstance(rows, list):
            rows = []
        hit = next((row for row in rows if str(row.get("symbol") or "").lower() == base), None)
        if not hit and rows:
            hit = rows[0]
        if not hit:
            return {}
        return {
            "name": hit.get("name"),
            "market_cap": hit.get("market_cap"),
            "circulating_supply": hit.get("circulating_supply"),
            "total_supply": hit.get("total_supply"),
            "max_supply": hit.get("max_supply"),
            "quote_volume": hit.get("total_volume"),
            "last": hit.get("current_price"),
            "percentage": hit.get("price_change_percentage_24h"),
        }

    return _cached(f"cg:meta:{base}", 600, load) or {}


def _yahoo_stats(symbol: str) -> dict[str, Any]:
    if is_crypto(symbol):
        ysym = f"{_crypto_base(symbol)}-USD"
    else:
        ysym = symbol

    def load() -> dict[str, Any]:
        try:
            payload = _get_json(
                "https://query1.finance.yahoo.com/v7/finance/quote?symbols=" + ysym
            )
        except Exception:
            return {}
        item = (((payload.get("quoteResponse") or {}).get("result")) or [None])[0] or {}
        if not item:
            return {}
        return {
            "name": item.get("shortName") or item.get("longName"),
            "market_cap": item.get("marketCap"),
            "shares_outstanding": item.get("sharesOutstanding"),
            "shares_float": item.get("floatShares"),
            "circulating_supply": item.get("circulatingSupply"),
            "avg_volume": item.get("averageDailyVolume3Month") or item.get("averageDailyVolume10Day"),
            "last": item.get("regularMarketPrice"),
            "percentage": item.get("regularMarketChangePercent"),
            "volume": item.get("regularMarketVolume"),
            "sector": item.get("sector"),
            "industry": item.get("industry"),
        }

    return _cached(f"yahoo:stats:{ysym}", 180, load) or {}


def _tape_metrics(symbol: str, timeframe: str) -> dict[str, Any]:
    def load() -> dict[str, Any]:
        rows = fetch_ohlcv(symbol, timeframe, 80)
        mood = _sentiment_from_bars(rows)
        if len(rows) < 16:
            return {
                "sentiment": mood,
                "momentum": {"value": None, "rsi": None, "label": "momNeutral", "volume_ratio": None},
            }
        frame = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
        close = frame["close"]
        rsi_raw = rsi(close, 14).iloc[-1]
        rsi_now = 50.0 if pd.isna(rsi_raw) else float(rsi_raw)
        prev = float(close.iloc[-11]) if len(close) > 11 else float(close.iloc[0])
        last = float(close.iloc[-1] or 0)
        mom_pct = ((last / prev - 1) * 100) if prev else 0.0
        vol = frame["volume"]
        avg = float(vol.tail(20).mean() or 0)
        last_vol = float(vol.iloc[-1] or 0)
        volume_ratio = (last_vol / avg) if avg else 1.0
        if rsi_now >= 70:
            label = "momOverbought"
        elif rsi_now <= 30:
            label = "momOversold"
        elif mom_pct > 0 and rsi_now >= 52:
            label = "momBullish"
        elif mom_pct < 0 and rsi_now <= 48:
            label = "momBearish"
        else:
            label = "momNeutral"
        return {
            "sentiment": mood,
            "momentum": {
                "value": round(mom_pct, 3),
                "rsi": round(rsi_now, 1),
                "label": label,
                "volume_ratio": round(volume_ratio, 3),
            },
        }

    return _cached(f"tape:{symbol}:{timeframe}", 45, load)


def _first(*values: Any) -> Any:
    for value in values:
        if value is None or value == "":
            continue
        return value
    return None


def fundamentals(symbol: str, timeframe: str = "1h") -> dict[str, Any]:
    tape = _tape_metrics(symbol, timeframe)
    mood = tape.get("sentiment") or sentiment(symbol, timeframe)
    momentum_pack = tape.get("momentum") or {}
    extra = _yahoo_stats(symbol)

    if is_crypto(symbol):
        from apps.api.app.services.scanner import CRYPTO_SECTORS, crypto_universe

        row = next((item for item in crypto_universe() if item["symbol"] == symbol), None) or {}
        cg = _crypto_meta(symbol)
        base = _crypto_base(symbol)
        supply = _first(cg.get("circulating_supply"), extra.get("circulating_supply"))
        total = cg.get("total_supply")
        quote_volume = _first(cg.get("quote_volume"), row.get("quote_volume"))
        return {
            "symbol": symbol,
            "venue": "crypto",
            "name": cg.get("name") or row.get("name") or extra.get("name") or base,
            "last": _first(row.get("last"), extra.get("last"), cg.get("last")),
            "percentage": _first(row.get("percentage"), extra.get("percentage"), cg.get("percentage")),
            "volume": row.get("volume"),
            "quote_volume": quote_volume,
            "avg_volume": extra.get("avg_volume"),
            "market_cap": _first(cg.get("market_cap"), extra.get("market_cap"), row.get("market_cap")),
            "supply": supply,
            "total_supply": total,
            "shares_outstanding": None,
            "shares_float": None,
            "pe": None,
            "sector": CRYPTO_SECTORS.get(base),
            "industry": CRYPTO_SECTORS.get(base),
            "sentiment": mood,
            "liquidity": {
                "quote_volume": quote_volume,
                "volume_ratio": momentum_pack.get("volume_ratio"),
                "score": mood.get("score"),
                "bias": mood.get("bias"),
            },
            "momentum": momentum_pack,
            "timeframe": timeframe,
        }

    row = stocks.stock_fundamentals(symbol) or {}
    quote_volume = _first(row.get("quote_volume"), extra.get("volume"), row.get("volume"))
    return {
        "symbol": symbol,
        "venue": row.get("venue") or stocks.venue_of(symbol),
        "name": row.get("name") or extra.get("name") or symbol,
        "last": _first(row.get("last"), extra.get("last")),
        "percentage": _first(row.get("percentage"), extra.get("percentage")),
        "volume": _first(row.get("volume"), extra.get("volume")),
        "quote_volume": quote_volume,
        "avg_volume": _first(row.get("avg_volume"), extra.get("avg_volume")),
        "market_cap": _first(row.get("market_cap"), extra.get("market_cap")),
        "supply": None,
        "total_supply": None,
        "shares_outstanding": _first(row.get("shares_outstanding"), extra.get("shares_outstanding")),
        "shares_float": _first(row.get("shares_float"), extra.get("shares_float")),
        "pe": row.get("pe"),
        "sector": row.get("sector") or extra.get("sector"),
        "industry": row.get("industry") or extra.get("industry"),
        "sentiment": mood,
        "liquidity": {
            "quote_volume": quote_volume,
            "volume_ratio": momentum_pack.get("volume_ratio"),
            "score": mood.get("score"),
            "bias": mood.get("bias"),
        },
        "momentum": momentum_pack,
        "timeframe": timeframe,
    }
