from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

import numpy as np
import pandas as pd

from indicators.momentum import ema, macd, rsi
from indicators.volatility import atr

Direction = Literal["bullish", "bearish", "neutral"]


@dataclass
class AgentOpinion:
    source: str
    direction: Direction
    confidence: float
    win_probability: float
    reasoning_en: str
    reasoning_ar: str
    suggested_entry: float | None
    suggested_stop_loss: float | None
    suggested_take_profits: list[float]
    metadata: dict[str, Any]


def _ohlcv_to_df(candles: list[dict[str, Any]]) -> pd.DataFrame:
    df = pd.DataFrame(candles)
    return df.sort_values("timestamp_ms").reset_index(drop=True)


def _dir_from_score(score: float, threshold: float = 0.12) -> Direction:
    if score > threshold:
        return "bullish"
    if score < -threshold:
        return "bearish"
    return "neutral"


def _levels(df: pd.DataFrame, direction: Direction, atr_mult: float = 1.6) -> tuple[float, float | None, list[float]]:
    entry = float(df["close"].iloc[-1])
    atr_now = float(atr(df).iloc[-1])
    if np.isnan(atr_now) or atr_now <= 0:
        return entry, None, []
    dist = atr_now * atr_mult
    if direction == "bullish":
        return entry, entry - dist, [entry + dist, entry + 2 * dist, entry + 3 * dist]
    if direction == "bearish":
        return entry, entry + dist, [entry - dist, entry - 2 * dist, entry - 3 * dist]
    return entry, None, []


def quant_agent(df: pd.DataFrame) -> AgentOpinion:
    """Classical quant stack: EMA trend, MACD, RSI, ATR volatility regime."""
    closes = df["close"]
    ema_fast = ema(closes, 12).iloc[-1]
    ema_slow = ema(closes, 26).iloc[-1]
    macd_df = macd(closes)
    hist = float(macd_df["histogram"].iloc[-1])
    rsi_now = float(rsi(closes).iloc[-1])
    atr_now = float(atr(df).iloc[-1])
    atr_pct = atr_now / float(closes.iloc[-1]) if closes.iloc[-1] else 0

    score = 0.0
    score += 0.35 if ema_fast > ema_slow else -0.35
    score += 0.30 if hist > 0 else -0.30
    if rsi_now < 32:
        score += 0.25
    elif rsi_now > 68:
        score -= 0.25
    if atr_pct > 0.035:
        score *= 0.85  # choppy regime discount

    direction = _dir_from_score(score)
    confidence = min(0.92, abs(score) + 0.15)
    win_probability = 0.50 + (confidence - 0.15) * 0.28
    entry, sl, tps = _levels(df, direction)
    return AgentOpinion(
        source="quant",
        direction=direction,
        confidence=round(confidence, 3),
        win_probability=round(min(0.78, max(0.42, win_probability)), 3),
        reasoning_en=(
            f"EMA12/26 {'bullish' if ema_fast > ema_slow else 'bearish'}, "
            f"MACD hist {hist:+.4f}, RSI {rsi_now:.1f}, ATR {atr_pct:.2%} of price."
        ),
        reasoning_ar=(
            f"متوسطا EMA 12/26 {'صاعدان' if ema_fast > ema_slow else 'هابطان'}، "
            f"هيستوغرام MACD {hist:+.4f}، RSI {rsi_now:.1f}، التقلب ATR {atr_pct:.2%} من السعر."
        ),
        suggested_entry=entry,
        suggested_stop_loss=sl,
        suggested_take_profits=tps,
        metadata={"rsi": rsi_now, "macd_hist": hist, "atr_pct": atr_pct},
    )


def pattern_agent(df: pd.DataFrame) -> AgentOpinion:
    """Engulfing + swing structure (HH/HL vs LH/LL) — not a 20-pattern library."""
    if len(df) < 30:
        return AgentOpinion(
            source="pattern",
            direction="neutral",
            confidence=0.2,
            win_probability=0.5,
            reasoning_en="Not enough candles for structure.",
            reasoning_ar="الشموع غير كافية لتحليل البنية.",
            suggested_entry=float(df["close"].iloc[-1]),
            suggested_stop_loss=None,
            suggested_take_profits=[],
            metadata={},
        )

    prev, curr = df.iloc[-2], df.iloc[-1]
    engulf = None
    if prev["close"] < prev["open"] and curr["close"] > curr["open"] and curr["close"] >= prev["open"] and curr["open"] <= prev["close"]:
        engulf = "bullish_engulfing"
    elif prev["close"] > prev["open"] and curr["close"] < curr["open"] and curr["open"] >= prev["close"] and curr["close"] <= prev["open"]:
        engulf = "bearish_engulfing"

    swing_highs = df["high"].rolling(5).max()
    swing_lows = df["low"].rolling(5).min()
    hh = swing_highs.iloc[-1] > swing_highs.iloc[-8]
    hl = swing_lows.iloc[-1] > swing_lows.iloc[-8]
    lh = swing_highs.iloc[-1] < swing_highs.iloc[-8]
    ll = swing_lows.iloc[-1] < swing_lows.iloc[-8]

    score = 0.0
    if hh and hl:
        score += 0.4
    if lh and ll:
        score -= 0.4
    if engulf == "bullish_engulfing":
        score += 0.35
    if engulf == "bearish_engulfing":
        score -= 0.35

    direction = _dir_from_score(score)
    confidence = min(0.88, abs(score) + 0.2)
    entry, sl, tps = _levels(df, direction, atr_mult=1.4)
    return AgentOpinion(
        source="pattern",
        direction=direction,
        confidence=round(confidence, 3),
        win_probability=round(0.48 + abs(score) * 0.35, 3),
        reasoning_en=(
            f"Structure: HH={hh} HL={hl} LH={lh} LL={ll}. Pattern={engulf or 'none'}."
        ),
        reasoning_ar=(
            f"البنية: قمم أعلى={hh} قيعان أعلى={hl} قمم أدنى={lh} قيعان أدنى={ll}. النمط={engulf or 'لا يوجد'}."
        ),
        suggested_entry=entry,
        suggested_stop_loss=sl,
        suggested_take_profits=tps,
        metadata={"engulfing": engulf, "hh": hh, "hl": hl, "lh": lh, "ll": ll},
    )


def liquidity_agent(df: pd.DataFrame, book: dict[str, Any] | None = None) -> AgentOpinion:
    """Volume climax + bid/ask wall imbalance. Approximates liquidity, not full footprint."""
    vol = df["volume"]
    vol_sma = vol.rolling(20).mean().iloc[-1]
    last_vol = float(vol.iloc[-1])
    spike = (last_vol / vol_sma) if vol_sma and vol_sma > 0 else 1.0
    close = float(df["close"].iloc[-1])
    open_ = float(df["open"].iloc[-1])
    close_bias = 1 if close > open_ else -1

    book_score = 0.0
    wall_note_en = "No live book."
    wall_note_ar = "لا يوجد دفتر أوامر لحظي."
    if book and book.get("bids") and book.get("asks"):
        bid_vol = sum(x["amount"] for x in book["bids"])
        ask_vol = sum(x["amount"] for x in book["asks"])
        total = bid_vol + ask_vol
        imbalance = (bid_vol - ask_vol) / total if total else 0
        book_score = float(np.clip(imbalance, -1, 1)) * 0.5
        top_bid = book["bids"][0]["amount"]
        top_ask = book["asks"][0]["amount"]
        avg_bid = bid_vol / max(len(book["bids"]), 1)
        avg_ask = ask_vol / max(len(book["asks"]), 1)
        wall_note_en = f"Book imbalance {imbalance:+.2f}; top bid {top_bid:.2f} vs avg {avg_bid:.2f}, top ask {top_ask:.2f} vs avg {avg_ask:.2f}."
        wall_note_ar = f"اختلال الدفتر {imbalance:+.2f}؛ أعلى طلب {top_bid:.2f} مقابل متوسط {avg_bid:.2f}، أعلى عرض {top_ask:.2f} مقابل متوسط {avg_ask:.2f}."

    vol_score = 0.2 * close_bias if spike >= 2.2 else 0.0
    score = book_score + vol_score
    direction = _dir_from_score(score, threshold=0.08)
    confidence = min(0.9, abs(score) + min(spike / 8, 0.25) + 0.2)
    entry, sl, tps = _levels(df, direction, atr_mult=1.2)
    return AgentOpinion(
        source="liquidity",
        direction=direction,
        confidence=round(confidence, 3),
        win_probability=round(0.47 + abs(score) * 0.4, 3),
        reasoning_en=f"Volume spike {spike:.1f}x 20-bar avg. {wall_note_en}",
        reasoning_ar=f"طفرة حجم {spike:.1f}× متوسط 20 شمعة. {wall_note_ar}",
        suggested_entry=entry,
        suggested_stop_loss=sl,
        suggested_take_profits=tps,
        metadata={"volume_spike": spike, "book_score": book_score},
    )


def consensus(opinions: list[AgentOpinion]) -> dict[str, Any]:
    bull = sum(o.confidence for o in opinions if o.direction == "bullish")
    bear = sum(o.confidence for o in opinions if o.direction == "bearish")
    if bull > bear and bull >= 0.5:
        direction: Direction = "bullish"
        score = bull
    elif bear > bull and bear >= 0.5:
        direction = "bearish"
        score = bear
    else:
        direction = "neutral"
        score = max(bull, bear)
    best = max(opinions, key=lambda o: o.confidence)
    win = float(np.mean([o.win_probability for o in opinions]))
    if direction == "neutral":
        win = 0.5
    return {
        "direction": direction,
        "confidence": round(min(0.95, score / max(len(opinions), 1) + 0.1), 3),
        "win_probability": round(win if direction != "neutral" else 0.5, 3),
        "entry": best.suggested_entry,
        "stop_loss": best.suggested_stop_loss if direction != "neutral" else None,
        "take_profits": best.suggested_take_profits if direction != "neutral" else [],
        "reasoning_en": f"Weighted consensus {direction}. Lead agent: {best.source}.",
        "reasoning_ar": f"إجماع مرجح: {direction}. الوكيل الأبرز: {best.source}.",
    }


def run_swarm(candles: list[dict[str, Any]], book: dict[str, Any] | None = None) -> dict[str, Any]:
    df = _ohlcv_to_df(candles)
    if len(df) < 40:
        raise ValueError("Need at least 40 candles for SHC agents")
    opinions = [quant_agent(df), pattern_agent(df), liquidity_agent(df, book)]
    payload = {
        "opinions": [
            {
                "source": o.source,
                "direction": o.direction,
                "confidence": o.confidence,
                "win_probability": o.win_probability,
                "reasoning_en": o.reasoning_en,
                "reasoning_ar": o.reasoning_ar,
                "suggested_entry": o.suggested_entry,
                "suggested_stop_loss": o.suggested_stop_loss,
                "suggested_take_profits": o.suggested_take_profits,
                "metadata": o.metadata,
            }
            for o in opinions
        ],
        "consensus": consensus(opinions),
        "last_close": float(df["close"].iloc[-1]),
        "bars": len(df),
    }
    return payload
