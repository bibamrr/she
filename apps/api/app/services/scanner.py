from __future__ import annotations

from typing import Any

from apps.api.app.services import stocks
from apps.api.app.services.market import fetch_crypto_tickers, parse_market_symbol
from apps.api.app.services.stables import skip_crypto_hunter
from apps.api.app.services.yahoo import SAUDI_UNIVERSE, _cached, rank_rows

EQUITY_VENUES = ("us", "tadawul", "europe", "asia", "commodities")

CRYPTO_SECTORS = {
    "BTC": "Layer 1",
    "ETH": "Layer 1",
    "SOL": "Layer 1",
    "ADA": "Layer 1",
    "AVAX": "Layer 1",
    "DOT": "Layer 1",
    "NEAR": "Layer 1",
    "ATOM": "Layer 1",
    "TON": "Layer 1",
    "SUI": "Layer 1",
    "APT": "Layer 1",
    "BNB": "Exchange",
    "CRO": "Exchange",
    "UNI": "DeFi",
    "AAVE": "DeFi",
    "MKR": "DeFi",
    "CRV": "DeFi",
    "LDO": "DeFi",
    "LINK": "Oracle",
    "DOGE": "Meme",
    "SHIB": "Meme",
    "PEPE": "Meme",
    "WIF": "Meme",
    "XRP": "Payments",
    "XLM": "Payments",
    "LTC": "Payments",
    "TRX": "Payments",
    "RENDER": "AI",
    "FET": "AI",
    "TAO": "AI",
    "ARB": "L2",
    "OP": "L2",
    "MATIC": "L2",
    "POL": "L2",
    "FIL": "Storage",
}


def crypto_universe() -> list[dict[str, Any]]:
    def load():
        tickers = fetch_crypto_tickers()
        rows = []
        for symbol, data in tickers.items():
            if not symbol.endswith("/USDT") or symbol.count("/") != 1:
                continue
            if any(tag in symbol for tag in ("UP/", "DOWN/", "BULL/", "BEAR/")):
                continue
            last = data.get("last") or 0
            qvol = data.get("quoteVolume") or 0
            rows.append(
                {
                    "symbol": symbol,
                    "name": symbol.split("/")[0],
                    "last": last,
                    "percentage": data.get("percentage"),
                    "volume": data.get("baseVolume"),
                    "quote_volume": qvol,
                    "market_cap": qvol,
                    "venue": "crypto",
                    "exchange": "binance",
                    "market_type": "spot",
                }
            )
        return rows

    return _cached("crypto_tickers", 45, load)


def crypto_tradeable() -> list[dict[str, Any]]:
    """Spot crypto minus stables and $1 pegs — used by hunter and market ranks."""
    return [row for row in crypto_universe() if not skip_crypto_hunter(row.get("symbol") or "", row)]


def crypto_sectors() -> list[dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = {}
    for row in crypto_tradeable():
        base = row["symbol"].split("/")[0]
        name = CRYPTO_SECTORS.get(base, "Other")
        buckets.setdefault(name, []).append(row)
    ranked = []
    for name, items in buckets.items():
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
                "venue": "crypto",
            }
        )
    ranked.sort(key=lambda item: item["percentage"], reverse=True)
    return ranked[:12]


def scan_crypto() -> dict[str, Any]:
    rows = crypto_tradeable()
    ranked = rank_rows(rows)
    ranked["all_count"] = len(rows)
    ranked["venue"] = "crypto"
    ranked["sectors"] = crypto_sectors()
    return ranked


def scan_us() -> dict[str, Any]:
    try:
        return stocks.scan("us")
    except Exception as exc:  # noqa: BLE001
        return {"gainers": [], "losers": [], "mcap": [], "active": [], "sectors": [], "venue": "us", "all_count": 0, "warning": str(exc)}


def scan_tadawul() -> dict[str, Any]:
    return scan_desk("tadawul")


def scan_desk(venue: str) -> dict[str, Any]:
    empty = {"gainers": [], "losers": [], "mcap": [], "active": [], "sectors": [], "venue": venue, "all_count": 0}
    try:
        return stocks.scan(venue)
    except Exception as exc:  # noqa: BLE001
        empty["warning"] = str(exc)
        return empty


def search_assets(query: str) -> list[dict[str, Any]]:
    """Search every desk at once and tag each hit with the venue that owns it."""
    q = query.strip().upper()
    if not q:
        return []
    hits: list[dict[str, Any]] = []
    for row in crypto_universe():
        if q in row["symbol"].upper() or q in row["name"].upper():
            hits.append(row)
        if len(hits) >= 10:
            break
    try:
        hits.extend(stocks.search(query, limit=16))
    except Exception:
        for symbol, name in SAUDI_UNIVERSE:
            if q in symbol.upper() or q in name:
                hits.append({"symbol": symbol, "name": name, "venue": "tadawul"})
        for spec in stocks.COMMODITIES:
            if q in spec["symbol"].upper() or q in spec["name"].upper():
                hits.append({"symbol": spec["symbol"], "name": spec["name"], "venue": "commodities"})

    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for item in hits:
        key = item.get("symbol")
        if key and key not in seen:
            seen.add(key)
            unique.append(item)
            spec = parse_market_symbol(key)
            if spec["crypto"] and spec["market_type"] == "spot":
                fut = f"{spec['display']}:FUT"
                if fut not in seen:
                    seen.add(fut)
                    unique.append(
                        {
                            **item,
                            "symbol": fut,
                            "name": item.get("name") or spec["display"].split("/")[0],
                            "exchange": "binance",
                            "market_type": "futures",
                            "last": None,
                            "percentage": None,
                        }
                    )
    return unique[:24]
