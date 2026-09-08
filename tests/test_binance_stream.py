from __future__ import annotations

from apps.api.app.services.binance_stream import parse_tick, stream_id, stream_url


def test_stream_url_uses_public_vision_host() -> None:
    url = stream_url(["BTC/USDT"])
    assert url.startswith("wss://data-stream.binance.vision/stream?streams=")
    assert "btcusdt@aggTrade" in url
    assert stream_id("BTC/USDT:FUT") == "btcusdt"


def test_parse_agg_trade() -> None:
    tick = parse_tick(
        {"stream": "xrpusdt@aggTrade", "data": {"e": "aggTrade", "s": "XRPUSDT", "p": "2.51", "E": 1700000000000}},
        {"xrpusdt": "XRP/USDT"},
    )
    assert tick is not None
    assert tick["symbol"] == "XRP/USDT"
    assert tick["price"] == 2.51
