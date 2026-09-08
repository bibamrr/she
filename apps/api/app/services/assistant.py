"""In-app SHC assistant.

It always answers from live desk data (VRCS state, Brain confluence, Hunter hits,
win-rate history). When ``SHC_ASSISTANT_PROVIDER`` is anthropic/openai the same
data is handed to the model as grounded context; otherwise the built-in
explanation engine answers locally with no external dependency.
"""

from __future__ import annotations

import json
import urllib.request
from typing import Any

from apps.api.app.config import get_settings
from apps.api.app.services.hunter import backtest, hunt, multi_timeframe

INTENTS = {
    "hunter": ("صياد", "الصياد", "فرص", "hunter", "scan", "opportunit"),
    "brain": ("عقل", "العقل", "توافق", "فريم", "confluence", "brain", "timeframe"),
    "history": ("سجل", "نجاح", "backtest", "win", "history", "نسبة"),
    "signal": ("إشارة", "اشارة", "احتقان", "زنبرك", "vrcs", "signal", "spring", "compression"),
    "help": ("كيف", "ماذا", "شرح", "help", "what", "how"),
}


def _intents(question: str) -> set[str]:
    """Every topic the question touches, so a compound question gets a full answer."""
    text = question.lower()
    found = {name for name, keys in INTENTS.items() if any(key in text for key in keys)}
    if not found or found == {"help"}:
        found |= {"brain", "hunter", "history", "signal"}
    return found


def _fmt_pct(value: Any) -> str:
    try:
        return f"{float(value):.1f}%"
    except (TypeError, ValueError):
        return "—"


def gather_context(symbol: str, timeframe: str) -> dict[str, Any]:
    tf = "1m" if timeframe == "1s" else timeframe
    context: dict[str, Any] = {"symbol": symbol, "timeframe": tf}
    try:
        context["confluence"] = multi_timeframe(symbol, ["15m", "1h", "4h"])
    except Exception as exc:  # noqa: BLE001
        context["confluence_error"] = str(exc)
    try:
        report = backtest(symbol, tf, 24, 2.0)
        context["history"] = {
            "win_rate": report["win_rate"],
            "high_confidence_win_rate": report["high_confidence_win_rate"],
            "total_signals": report["total_signals"],
            "closed": report["closed"],
            "avg_pnl_pct": report["avg_pnl_pct"],
            "buckets": report["buckets"],
        }
    except Exception as exc:  # noqa: BLE001
        context["history_error"] = str(exc)
    try:
        scan = hunt(tf, 40, 75.0, 2.0)
        context["hunter"] = {
            "scanned": scan["scanned"],
            "elite": [h["symbol"] for h in scan["elite"]],
            "top": [
                {"symbol": h["symbol"], "state": h["state"], "confidence": h["confidence"], "volume_ratio": h["volume_ratio"]}
                for h in scan["hits"][:6]
            ],
            "quiet_surges": [h["symbol"] for h in scan["quiet_surges"]],
        }
    except Exception as exc:  # noqa: BLE001
        context["hunter_error"] = str(exc)
    return context


def _local_answer(question: str, context: dict[str, Any], locale: str) -> str:
    intents = _intents(question)
    ar = locale == "ar"
    symbol = context["symbol"]
    tf = context["timeframe"]
    conf = context.get("confluence") or {}
    hist = context.get("history") or {}
    hunter = context.get("hunter") or {}
    lines: list[str] = []

    if intents & {"brain", "signal"}:
        direction = conf.get("direction", "neutral")
        aligned = ", ".join(conf.get("aligned_frames") or []) or ("لا شيء" if ar else "none")
        coiled = ", ".join(conf.get("coiled_frames") or []) or ("لا شيء" if ar else "none")
        if ar:
            lines.append(
                f"العقل على {symbol} ({tf}): الاتجاه {direction} بثقة {_fmt_pct(conf.get('confluence_confidence'))}."
            )
            lines.append(f"فريمات متوافقة: {aligned} · فريمات محتقنة: {coiled}.")
        else:
            lines.append(
                f"Brain on {symbol} ({tf}): {direction} at {_fmt_pct(conf.get('confluence_confidence'))} confluence."
            )
            lines.append(f"Aligned frames: {aligned} · coiled frames: {coiled}.")
        for frame in conf.get("frames", [])[:4]:
            state = frame.get("regime")
            lines.append(
                f"· {frame.get('timeframe')}: {state} — {_fmt_pct(frame.get('confidence'))}"
                + (f" ({frame.get('bars_since_signal')} bars since spring)" if frame.get("bars_since_signal") is not None else "")
            )

    if "hunter" in intents and hunter:
        elite = ", ".join(hunter.get("elite") or []) or ("لا فرص نخبة الآن" if ar else "no elite setups right now")
        surges = ", ".join(hunter.get("quiet_surges") or []) or ("—")
        if ar:
            lines.append(f"الصياد مسح {hunter.get('scanned')} عملة. فرص 90%+: {elite}.")
            lines.append(f"تدفق حجمي في شموع هادئة: {surges}.")
        else:
            lines.append(f"Hunter scanned {hunter.get('scanned')} symbols. 90%+ setups: {elite}.")
            lines.append(f"Quiet-candle volume surges: {surges}.")
        for hit in hunter.get("top", [])[:5]:
            lines.append(f"· {hit['symbol']}: {hit['state']} {hit['confidence']}% (vol x{hit['volume_ratio']})")

    if "history" in intents and hist:
        if ar:
            lines.append(
                f"السجل على {symbol} {tf}: نسبة النجاح {_fmt_pct(hist.get('win_rate'))} من {hist.get('closed')} فرصة مغلقة،"
                f" وشريحة 90%+ نجاحها {_fmt_pct(hist.get('high_confidence_win_rate'))}."
            )
        else:
            lines.append(
                f"History on {symbol} {tf}: {_fmt_pct(hist.get('win_rate'))} win rate over {hist.get('closed')} closed"
                f" setups; the 90%+ bucket wins {_fmt_pct(hist.get('high_confidence_win_rate'))}."
            )

    if not lines:
        lines.append("لا توجد بيانات كافية الآن." if ar else "Not enough desk data right now.")

    if "signal" in intents:
        tail = (
            "القراءة العملية: الاحتقان يعني تجميعاً صامتاً — انتظر إغلاقاً خارج النطاق مع حجم أعلى من المتوسط،"
            " والثقة 90%+ هي التي تستحق التنبيه."
            if ar
            else "Read it this way: compression means silent accumulation — wait for a close outside the range with"
            " above-average volume; only 90%+ confidence deserves an alert."
        )
        lines.append(tail)
    return "\n".join(lines)


def _llm_answer(question: str, context: dict[str, Any], locale: str) -> str | None:
    settings = get_settings()
    provider = settings.assistant_provider.lower()
    if provider not in {"anthropic", "openai"} or not settings.assistant_api_key:
        return None
    system = (
        "You are the SHC desk assistant. Explain VRCS compression, spring signals, Brain confluence and "
        "Hunter results using ONLY the JSON context. Be concise and concrete. "
        f"Answer in {'Arabic' if locale == 'ar' else 'English'}."
    )
    prompt = f"Question: {question}\n\nDesk context JSON:\n{json.dumps(context, ensure_ascii=False)[:12000]}"
    try:
        if provider == "anthropic":
            request = urllib.request.Request(
                "https://api.anthropic.com/v1/messages",
                data=json.dumps(
                    {
                        "model": settings.assistant_model,
                        "max_tokens": 700,
                        "system": system,
                        "messages": [{"role": "user", "content": prompt}],
                    }
                ).encode(),
                headers={
                    "x-api-key": settings.assistant_api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
            )
            with urllib.request.urlopen(request, timeout=45) as response:
                data = json.loads(response.read().decode())
            return "".join(block.get("text", "") for block in data.get("content", [])) or None
        request = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(
                {
                    "model": settings.assistant_model,
                    "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
                    "max_tokens": 700,
                }
            ).encode(),
            headers={
                "Authorization": f"Bearer {settings.assistant_api_key}",
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(request, timeout=45) as response:
            data = json.loads(response.read().decode())
        return data["choices"][0]["message"]["content"]
    except Exception:  # noqa: BLE001
        return None


def ask(question: str, symbol: str, timeframe: str, locale: str = "ar") -> dict[str, Any]:
    context = gather_context(symbol, timeframe)
    answer = _llm_answer(question, context, locale)
    engine = get_settings().assistant_provider.lower() if answer else "local"
    if not answer:
        answer = _local_answer(question, context, locale)
    return {
        "question": question,
        "answer": answer,
        "engine": engine,
        "symbol": symbol,
        "timeframe": context["timeframe"],
        "context": {
            "direction": (context.get("confluence") or {}).get("direction"),
            "confluence_confidence": (context.get("confluence") or {}).get("confluence_confidence"),
            "win_rate": (context.get("history") or {}).get("win_rate"),
            "elite": (context.get("hunter") or {}).get("elite", []),
        },
    }
