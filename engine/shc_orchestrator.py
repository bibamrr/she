from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from engine.coordinator import display_name, vote_from_direction
from indicators.momentum import ema, macd, rsi
from indicators.volatility import atr

_NEWS_BUY = (
    "surge",
    "rally",
    "approval",
    "etf",
    "bull",
    "record",
    "beat",
    "partnership",
    "صعود",
    "ارتفاع",
    "إيجاب",
)
_NEWS_SELL = (
    "crash",
    "hack",
    "lawsuit",
    "ban",
    "sec",
    "dump",
    "default",
    "collapse",
    "هبوط",
    "انهيار",
    "حظر",
)


def ohlcv_to_df(rows: list[list[Any]]) -> pd.DataFrame:
    df = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    return df


def _attach_vote(agent: dict[str, Any]) -> dict[str, Any]:
    direction = str(agent.get("direction") or "neutral")
    agent["vote"] = agent.get("vote") or vote_from_direction(direction)
    agent["agent_name"] = agent.get("agent_name") or display_name(str(agent.get("name") or ""))
    return agent


def _direction_from_score(score: float) -> str:
    if score >= 0.18:
        return "bullish"
    if score <= -0.18:
        return "bearish"
    return "neutral"


def _success_probability(confluence: int, rsi_ok: bool, volume_ok: bool, book_align: bool) -> float:
    base = 0.42 + confluence * 0.09
    if rsi_ok:
        base += 0.06
    if volume_ok:
        base += 0.07
    if book_align:
        base += 0.08
    return round(min(0.92, max(0.18, base)), 3)


def analyze_liquidity(df: pd.DataFrame, book: dict[str, Any] | None) -> dict[str, Any]:
    vol_sma = df["volume"].rolling(20).mean().iloc[-1]
    last_vol = float(df["volume"].iloc[-1])
    volume_ratio = float(last_vol / vol_sma) if vol_sma and vol_sma > 0 else 1.0

    bins = pd.cut(df["close"], bins=24)
    volume_profile = df.groupby(bins, observed=False)["volume"].sum()
    poc_interval = volume_profile.idxmax() if len(volume_profile) else None
    poc = float(poc_interval.mid) if poc_interval is not None else float(df["close"].iloc[-1])

    bid_wall = ask_wall = 0.0
    imbalance = 0.0
    if book and book.get("bids") and book.get("asks"):
        bids = book["bids"][:20]
        asks = book["asks"][:20]
        bid_vol = sum(float(a) for _, a in bids)
        ask_vol = sum(float(a) for _, a in asks)
        total = bid_vol + ask_vol
        imbalance = (bid_vol - ask_vol) / total if total else 0.0
        avg_bid = bid_vol / max(len(bids), 1)
        avg_ask = ask_vol / max(len(asks), 1)
        bid_wall = float(bids[0][1]) / avg_bid if avg_bid else 0.0
        ask_wall = float(asks[0][1]) / avg_ask if avg_ask else 0.0

    if imbalance > 0.18 or bid_wall >= 3.2:
        direction = "bullish"
        score = min(1.0, 0.45 + abs(imbalance) + (bid_wall / 10))
        thesis = "Bid-side liquidity and resting support dominate the visible book."
        reason_code = "liq_bid"
    elif imbalance < -0.18 or ask_wall >= 3.2:
        direction = "bearish"
        score = min(1.0, 0.45 + abs(imbalance) + (ask_wall / 10))
        thesis = "Ask-side liquidity / resistance wall is absorbing demand."
        reason_code = "liq_ask"
    else:
        direction = "neutral"
        score = 0.25
        thesis = "Book is two-sided; no durable liquidity edge."
        reason_code = "liq_flat"

    return _attach_vote(
        {
            "name": "liquidity_agent",
            "direction": direction,
            "confidence": round(min(0.95, score), 3),
            "reasoning": thesis,
            "reason_code": reason_code,
            "reason_params": {},
            "metrics": {
                "volume_ratio": round(volume_ratio, 3),
                "poc": round(poc, 6),
                "book_imbalance": round(imbalance, 4),
                "bid_wall_multiple": round(bid_wall, 3),
                "ask_wall_multiple": round(ask_wall, 3),
            },
        }
    )


def analyze_patterns(df: pd.DataFrame) -> dict[str, Any]:
    prev, curr = df.iloc[-2], df.iloc[-1]
    pattern = None
    if prev["close"] < prev["open"] and curr["close"] > curr["open"]:
        if curr["close"] >= prev["open"] and curr["open"] <= prev["close"]:
            pattern = "bullish_engulfing"
    if prev["close"] > prev["open"] and curr["close"] < curr["open"]:
        if curr["open"] >= prev["close"] and curr["close"] <= prev["open"]:
            pattern = "bearish_engulfing"

    body = abs(curr["close"] - curr["open"])
    wick_up = curr["high"] - max(curr["close"], curr["open"])
    wick_dn = min(curr["close"], curr["open"]) - curr["low"]
    if pattern is None and wick_dn > body * 2.2 and curr["close"] > curr["open"]:
        pattern = "hammer"
    if pattern is None and wick_up > body * 2.2 and curr["close"] < curr["open"]:
        pattern = "shooting_star"

    closes = df["close"].tail(30).to_numpy()
    x = np.arange(len(closes))
    slope = float(np.polyfit(x, closes, 1)[0] / np.mean(closes))

    if pattern in {"bullish_engulfing", "hammer"} or slope > 0.0006:
        direction = "bullish"
    elif pattern in {"bearish_engulfing", "shooting_star"} or slope < -0.0006:
        direction = "bearish"
    else:
        direction = "neutral"

    conf = 0.55 if pattern else 0.32
    if abs(slope) > 0.001:
        conf += 0.12

    return _attach_vote(
        {
            "name": "pattern_agent",
            "direction": direction,
            "confidence": round(min(0.9, conf), 3),
            "reasoning": f"Structure read: {pattern or 'no classical reversal'}; 30-bar slope={slope:.5f}.",
            "reason_code": "pattern_read",
            "reason_params": {"pattern": pattern or "none", "slope": f"{slope:.5f}"},
            "metrics": {"pattern": pattern or "none", "normalized_slope": round(slope, 6)},
        }
    )


def analyze_quant(df: pd.DataFrame) -> dict[str, Any]:
    close = df["close"]
    ema_fast = ema(close, 12).iloc[-1]
    ema_slow = ema(close, 26).iloc[-1]
    rsi_now = float(rsi(close, 14).iloc[-1])
    hist = float(macd(close)["histogram"].iloc[-1])
    atr_now = float(atr(df, 14).iloc[-1])
    last = float(close.iloc[-1])

    votes = 0.0
    votes += 1 if ema_fast > ema_slow else -1
    votes += 1 if hist > 0 else -1
    if rsi_now < 32:
        votes += 0.6
    elif rsi_now > 68:
        votes -= 0.6

    score = votes / 2.6
    direction = _direction_from_score(score)
    stop = last - atr_now * 1.5 if direction == "bullish" else last + atr_now * 1.5
    tps = (
        [last + atr_now * m for m in (1.0, 2.0, 3.0)]
        if direction == "bullish"
        else [last - atr_now * m for m in (1.0, 2.0, 3.0)]
    )

    return _attach_vote(
        {
            "name": "quant_agent",
            "direction": direction,
            "confidence": round(min(0.93, abs(score) + 0.35), 3),
            "reasoning": (
                f"EMA12/26 {'bull' if ema_fast > ema_slow else 'bear'}, "
                f"MACD hist {hist:+.5f}, RSI {rsi_now:.1f}, ATR {atr_now:.5f}."
            ),
            "reason_code": "quant_read",
            "reason_params": {
                "ema": "bull" if ema_fast > ema_slow else "bear",
                "hist": f"{hist:+.5f}",
                "rsi": f"{rsi_now:.1f}",
                "atr": f"{atr_now:.5f}",
            },
            "metrics": {
                "ema_fast": round(float(ema_fast), 6),
                "ema_slow": round(float(ema_slow), 6),
                "rsi": round(rsi_now, 2),
                "macd_histogram": round(hist, 6),
                "atr": round(atr_now, 6),
            },
            "entry": last,
            "stop_loss": round(float(stop), 6) if direction != "neutral" else None,
            "take_profits": [round(float(x), 6) for x in tps] if direction != "neutral" else [],
        }
    )


def analyze_radar(df: pd.DataFrame) -> dict[str, Any]:
    vol_avg = df["volume"].rolling(20).mean().iloc[-1]
    spike = float(df["volume"].iloc[-1] / vol_avg) if vol_avg else 1.0
    rsi_now = float(rsi(df["close"], 14).iloc[-1])
    alerts: list[str] = []
    if spike >= 2.4:
        alerts.append(f"volume_spike x{spike:.1f}")
    if rsi_now >= 72:
        alerts.append(f"rsi_overbought {rsi_now:.0f}")
    if rsi_now <= 28:
        alerts.append(f"rsi_oversold {rsi_now:.0f}")

    if "rsi_oversold" in " ".join(alerts) or spike >= 3:
        direction = "bullish" if rsi_now < 50 else "bearish"
        conf = 0.62
    elif "rsi_overbought" in " ".join(alerts):
        direction = "bearish"
        conf = 0.58
    else:
        direction = "neutral"
        conf = 0.28

    return _attach_vote(
        {
            "name": "radar_agent",
            "direction": direction,
            "confidence": conf,
            "reasoning": "; ".join(alerts) if alerts else "No anomaly vs 20-bar baseline.",
            "reason_code": "radar_alerts" if alerts else "radar_quiet",
            "reason_params": {"alerts": alerts, "rsi": f"{rsi_now:.0f}", "spike": f"{spike:.1f}"},
            "metrics": {"volume_spike": round(spike, 3), "rsi": round(rsi_now, 2), "alerts": alerts},
        }
    )


def analyze_news(headlines: list[dict[str, Any]] | None) -> dict[str, Any]:
    rows = headlines or []
    score = 0
    hits = 0
    for item in rows[:12]:
        title = str(item.get("title") or item.get("headline") or "").lower()
        if not title:
            continue
        hits += 1
        if any(word in title for word in _NEWS_BUY):
            score += 1
        if any(word in title for word in _NEWS_SELL):
            score -= 1
    if hits == 0:
        return _attach_vote(
            {
                "name": "news_sentiment_agent",
                "direction": "neutral",
                "confidence": 0.3,
                "reasoning": "No usable headlines in the news cache.",
                "reason_code": "news_empty",
                "reason_params": {},
                "metrics": {"headlines": 0},
            }
        )
    if score >= 2:
        direction, conf = "bullish", min(0.86, 0.55 + score * 0.08)
    elif score <= -2:
        direction, conf = "bearish", min(0.86, 0.55 + abs(score) * 0.08)
    else:
        direction, conf = "neutral", 0.38
    return _attach_vote(
        {
            "name": "news_sentiment_agent",
            "direction": direction,
            "confidence": round(conf, 3),
            "reasoning": f"Headline tilt {score:+d} across {hits} stories.",
            "reason_code": "news_tilt",
            "reason_params": {"score": f"{score:+d}", "hits": hits},
            "metrics": {"headlines": hits, "score": score},
        }
    )


def analyze_risk(df: pd.DataFrame, hunter: dict[str, Any] | None = None) -> dict[str, Any]:
    last = float(df["close"].iloc[-1])
    atr_now = float(atr(df, 14).iloc[-1] or 0)
    atr_pct = atr_now / last if last > 0 else 0.0
    bar = df.iloc[-1]
    range_pct = float(bar["high"] - bar["low"]) / last if last > 0 else 0.0
    hunter = hunter or {}
    stop = float(hunter.get("stop") or 0)
    entry = float(hunter.get("entry") or last)
    stop_dist = abs(entry - stop) / entry if entry > 0 and stop > 0 else 0.0

    if atr_pct >= 0.08 or range_pct >= 0.065:
        return _attach_vote(
            {
                "name": "risk_management_agent",
                "direction": "neutral",
                "confidence": 0.88,
                "reasoning": f"Volatility veto: ATR {atr_pct:.2%} / bar range {range_pct:.2%}.",
                "reason_code": "risk_vol",
                "reason_params": {"atr": f"{atr_pct:.2%}", "range": f"{range_pct:.2%}"},
                "metrics": {"atr_pct": round(atr_pct, 5), "range_pct": round(range_pct, 5), "veto": True},
            }
        )
    if atr_pct < 0.0008:
        return _attach_vote(
            {
                "name": "risk_management_agent",
                "direction": "neutral",
                "confidence": 0.84,
                "reasoning": "Dead-range veto: ATR too thin to justify a stop.",
                "reason_code": "risk_dead",
                "reason_params": {},
                "metrics": {"atr_pct": round(atr_pct, 5), "veto": True},
            }
        )
    if stop_dist and atr_now > 0 and stop_dist < (atr_now / entry) * 0.4:
        return _attach_vote(
            {
                "name": "risk_management_agent",
                "direction": "neutral",
                "confidence": 0.83,
                "reasoning": "Stop sits inside noise; Risk Management vetoes the setup.",
                "reason_code": "risk_stop",
                "reason_params": {},
                "metrics": {"stop_dist": round(stop_dist, 5), "veto": True},
            }
        )
    return _attach_vote(
        {
            "name": "risk_management_agent",
            "direction": "neutral",
            "confidence": 0.42,
            "reasoning": f"Risk acceptable. ATR {atr_pct:.2%}, stop distance {stop_dist:.2%}.",
            "reason_code": "risk_ok",
            "reason_params": {"atr": f"{atr_pct:.2%}", "stop": f"{stop_dist:.2%}"},
            "metrics": {"atr_pct": round(atr_pct, 5), "stop_dist": round(stop_dist, 5), "veto": False},
        }
    )


def analyze_market_sentiment(df: pd.DataFrame) -> dict[str, Any]:
    sample = df.tail(36)
    buy = float(sample.loc[sample["close"] >= sample["open"], "volume"].sum())
    sell = float(sample.loc[sample["close"] < sample["open"], "volume"].sum())
    total = buy + sell
    ratio = ((buy - sell) / total) if total else 0.0
    score = max(0.0, min(100.0, 50 + ratio * 50))
    if score >= 62:
        direction, conf = "bullish", min(0.88, 0.5 + (score - 62) / 80)
    elif score <= 38:
        direction, conf = "bearish", min(0.88, 0.5 + (38 - score) / 80)
    else:
        direction, conf = "neutral", 0.36
    return _attach_vote(
        {
            "name": "market_sentiment_agent",
            "direction": direction,
            "confidence": round(conf, 3),
            "reasoning": f"Tape sentiment {score:.0f} (buy {buy:.0f} / sell {sell:.0f}).",
            "reason_code": "tape_read",
            "reason_params": {"score": f"{score:.0f}", "buy": f"{buy:.0f}", "sell": f"{sell:.0f}"},
            "metrics": {"score": round(score, 1), "buy_volume": round(buy, 2), "sell_volume": round(sell, 2)},
        }
    )


def analyze_on_chain(df: pd.DataFrame, symbol: str) -> dict[str, Any]:
    crypto = "/" in (symbol or "") and str(symbol).upper().endswith(("USDT", "USDC", "BTC", "ETH"))
    if not crypto:
        return _attach_vote(
            {
                "name": "on_chain_agent",
                "direction": "neutral",
                "confidence": 0.28,
                "reasoning": "No on-chain tape for this venue; waiting.",
                "reason_code": "chain_none",
                "reason_params": {},
                "metrics": {"available": False},
            }
        )
    window = df.tail(24)
    delta = float((window["close"] - window["open"]).mul(window["volume"]).sum())
    vol = float(window["volume"].sum()) or 1.0
    flow = delta / vol
    last = float(df["close"].iloc[-1]) or 1.0
    flow_pct = flow / last
    if flow_pct > 0.004:
        direction, conf = "bullish", min(0.84, 0.52 + flow_pct * 20)
    elif flow_pct < -0.004:
        direction, conf = "bearish", min(0.84, 0.52 + abs(flow_pct) * 20)
    else:
        direction, conf = "neutral", 0.34
    return _attach_vote(
        {
            "name": "on_chain_agent",
            "direction": direction,
            "confidence": round(conf, 3),
            "reasoning": f"Spot flow proxy {flow_pct:.3%} from 24-bar volume delta — not raw chain data.",
            "reason_code": "chain_flow",
            "reason_params": {"flow": f"{flow_pct:.3%}"},
            "metrics": {"flow_pct": round(flow_pct, 6), "available": True},
        }
    )


def run_shc_analysis(
    symbol: str,
    timeframe: str,
    ohlcv: list[list[Any]],
    book: dict[str, Any] | None,
    extras: dict[str, Any] | None = None,
) -> dict[str, Any]:
    extras = extras or {}
    df = ohlcv_to_df(ohlcv)
    if len(df) < 40:
        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "direction": "neutral",
            "success_probability": 0.0,
            "reasoning": "Not enough history to run the swarm.",
            "reason_code": "thin_history",
            "reason_params": {},
            "agents": [],
        }

    agents = [
        analyze_radar(df),
        analyze_quant(df),
        analyze_patterns(df),
        analyze_liquidity(df, book),
        analyze_news(extras.get("news")),
        analyze_risk(df, extras.get("hunter")),
        analyze_market_sentiment(df),
        analyze_on_chain(df, symbol),
    ]

    bull = sum(a["confidence"] for a in agents if a["direction"] == "bullish")
    bear = sum(a["confidence"] for a in agents if a["direction"] == "bearish")
    if bull > bear and bull >= 0.7:
        direction = "bullish"
    elif bear > bull and bear >= 0.7:
        direction = "bearish"
    else:
        direction = "neutral"

    quant = next(a for a in agents if a["name"] == "quant_agent")
    liq = next(a for a in agents if a["name"] == "liquidity_agent")
    rsi_val = next(a for a in agents if a["name"] == "radar_agent")["metrics"]["rsi"]
    rsi_ok = (direction == "bullish" and rsi_val < 70) or (direction == "bearish" and rsi_val > 30)
    vol_ok = liq["metrics"]["volume_ratio"] >= 1.15
    book_ok = (direction == "bullish" and liq["metrics"]["book_imbalance"] > 0) or (
        direction == "bearish" and liq["metrics"]["book_imbalance"] < 0
    )
    confluence = sum(1 for a in agents if a["direction"] == direction)

    last = float(df["close"].iloc[-1])
    candles = [
        {
            "time": int(ts.timestamp()),
            "open": float(o),
            "high": float(h),
            "low": float(l),
            "close": float(c),
        }
        for ts, o, h, l, c in zip(df["timestamp"], df["open"], df["high"], df["low"], df["close"])
    ]
    ema12 = [None if pd.isna(v) else float(v) for v in ema(df["close"], 12).tolist()]
    ema26 = [None if pd.isna(v) else float(v) for v in ema(df["close"], 26).tolist()]
    rsi_series = [None if pd.isna(v) else float(v) for v in rsi(df["close"], 14).tolist()]

    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "last_price": last,
        "direction": direction,
        "success_probability": _success_probability(confluence, rsi_ok, vol_ok, book_ok)
        if direction != "neutral"
        else round(0.22 + confluence * 0.03, 3),
        "entry": quant.get("entry"),
        "stop_loss": quant.get("stop_loss"),
        "take_profits": quant.get("take_profits") or [],
        "reasoning": (
            f"Oracle consensus {direction.upper()} from {confluence}/8 agents. "
            f"Bull score {bull:.2f} vs bear {bear:.2f}."
        ),
        "reason_code": "oracle",
        "reason_params": {
            "direction": direction,
            "confluence": confluence,
            "bull": f"{bull:.2f}",
            "bear": f"{bear:.2f}",
        },
        "agents": agents,
        "overlays": {
            "ema12": ema12,
            "ema26": ema26,
            "rsi": rsi_series,
            "candles": candles,
        },
    }
