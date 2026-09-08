from __future__ import annotations

from apps.api.app.services.market import (
    _is_geo_blocked,
    _venue_symbol,
    parse_market_symbol,
)


def test_geo_block_detects_binance_451() -> None:
    err = RuntimeError(
        "451 Client Error: Service unavailable from a restricted location according to 'b. Eligibility'"
    )
    assert _is_geo_blocked(err) is True
    assert _is_geo_blocked(RuntimeError("timeout")) is False


def test_venue_symbol_maps_linear_perps() -> None:
    spec = parse_market_symbol("BTC/USDT:FUT")
    assert _venue_symbol("binance", spec) == "BTC/USDT:USDT"
    assert _venue_symbol("bybit", spec) == "BTC/USDT:USDT"
    assert _venue_symbol("okx", spec) == "BTC/USDT:USDT"
    spot = parse_market_symbol("ETH/USDT")
    assert _venue_symbol("bybit", spot) == "ETH/USDT"
