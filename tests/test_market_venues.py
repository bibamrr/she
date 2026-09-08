from __future__ import annotations

import ccxt

from apps.api.app.services.market import (
    _binance_url_overrides,
    _is_geo_blocked,
    _okx_inst_id,
    _venue_chain,
    _venue_symbol,
    binance_rest_v3_base,
    parse_market_symbol,
)


def test_geo_block_detects_binance_451() -> None:
    err = RuntimeError(
        "451 Client Error: Service unavailable from a restricted location according to 'b. Eligibility'"
    )
    assert _is_geo_blocked(err) is True
    assert _is_geo_blocked(RuntimeError("timeout")) is False


def test_geo_block_detects_bybit_403() -> None:
    class Forbidden(RuntimeError):
        http_status = 403

    assert _is_geo_blocked(Forbidden("403 Forbidden")) is True
    assert _is_geo_blocked(RuntimeError("403 from cloudfront")) is True


def test_binance_public_url_includes_api_v3() -> None:
    urls = _binance_url_overrides("https://data-api.binance.vision")
    assert urls["public"] == "https://data-api.binance.vision/api/v3"
    assert urls["v1"] == "https://data-api.binance.vision/api/v1"
    assert binance_rest_v3_base("https://data-api.binance.vision") == "https://data-api.binance.vision/api/v3"
    assert binance_rest_v3_base("https://data-api.binance.vision/api/v3") == "https://data-api.binance.vision/api/v3"

    client = ccxt.binance({"urls": {"api": urls}})
    signed = client.sign("exchangeInfo", "public", "GET", {}, {}, None)
    assert signed["url"] == "https://data-api.binance.vision/api/v3/exchangeInfo"


def test_venue_symbol_maps_linear_perps() -> None:
    spec = parse_market_symbol("BTC/USDT:FUT")
    assert _venue_symbol("binance", spec) == "BTC/USDT:USDT"
    assert _venue_symbol("bybit", spec) == "BTC/USDT:USDT"
    assert _venue_symbol("okx", spec) == "BTC-USDT-SWAP"
    assert _okx_inst_id(spec) == "BTC-USDT-SWAP"
    spot = parse_market_symbol("ETH/USDT")
    assert _venue_symbol("bybit", spot) == "ETH/USDT"
    assert _venue_symbol("okx", spot) == "ETH-USDT"


def test_futures_chain_skips_binance_without_proxy(monkeypatch) -> None:
    monkeypatch.setattr("apps.api.app.services.market._proxy_url", lambda: "")
    assert _venue_chain("spot")[0] == "binance"
    assert _venue_chain("futures") == ("okx", "kucoin", "bybit")
    assert "kucoin" in _venue_chain("spot")
