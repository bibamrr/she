"""Markets Overview: indices, crypto global stats, and batch quotes."""

from __future__ import annotations

from typing import Any

from apps.api.app.services import stocks
from apps.api.app.services.yahoo import _cached, _get_json


def crypto_global() -> dict[str, Any]:
    def load() -> dict[str, Any]:
        try:
            payload = _get_json("https://api.coingecko.com/api/v3/global")
            data = payload.get("data") or {}
            caps = data.get("total_market_cap") or {}
            vols = data.get("total_volume") or {}
            share = data.get("market_cap_percentage") or {}
            return {
                "total_market_cap": caps.get("usd"),
                "total_volume": vols.get("usd"),
                "btc_dominance": share.get("btc"),
                "eth_dominance": share.get("eth"),
                "source": "coingecko",
            }
        except Exception as exc:  # noqa: BLE001
            from apps.api.app.services.scanner import crypto_universe

            universe = crypto_universe()
            btc = next((row for row in universe if row["symbol"] == "BTC/USDT"), None)
            return {
                "total_market_cap": None,
                "total_volume": sum(float(row.get("quote_volume") or 0) for row in universe[:80]),
                "btc_dominance": None,
                "eth_dominance": None,
                "btc_last": (btc or {}).get("last"),
                "btc_percentage": (btc or {}).get("percentage"),
                "source": "binance-fallback",
                "warning": str(exc),
            }

    return _cached("crypto_global", 60, load)


def quotes(symbols: list[str]) -> list[dict[str, Any]]:
    wanted = [item.strip() for item in symbols if item and item.strip()][:40]
    if not wanted:
        return []
    from apps.api.app.services.market import fetch_ticker, parse_market_symbol
    from apps.api.app.services.scanner import crypto_universe

    crypto = {row["symbol"]: row for row in crypto_universe()}
    rows: list[dict[str, Any]] = []
    missing: list[str] = []
    for symbol in wanted:
        spec = parse_market_symbol(symbol)
        if spec["crypto"]:
            if spec["market_type"] == "spot":
                row = crypto.get(spec["display"]) or crypto.get(spec["desk"])
                if row:
                    rows.append(row)
                    continue
            missing.append(spec["desk"] or symbol)
            continue
        hit = stocks.quote(symbol)
        if hit:
            rows.append(hit)
        else:
            missing.append(symbol)
    if missing:
        desk_miss = []
        for item in missing:
            spec = parse_market_symbol(item)
            if spec["crypto"]:
                try:
                    ticker = fetch_ticker(item)
                    rows.append(
                        {
                            "symbol": ticker.get("symbol") or spec["desk"] or item,
                            "last": ticker.get("last"),
                            "percentage": ticker.get("percentage"),
                            "venue": "crypto",
                            "exchange": ticker.get("exchange") or "binance",
                            "market_type": ticker.get("market_type") or "spot",
                        }
                    )
                    continue
                except Exception:
                    pass
            desk_miss.append(item)
        if desk_miss:
            try:
                from apps.api.app.services.yahoo import yahoo_quote

                rows.extend(yahoo_quote(desk_miss))
            except Exception:
                pass
    return rows


def tape() -> dict[str, Any]:
    return {"indices": stocks.fetch_indices(), "crypto_global": crypto_global()}
