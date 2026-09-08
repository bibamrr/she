"""Transactional email for SHC (welcome, verification, subscription receipts).

Provider is chosen with ``SHC_EMAIL_PROVIDER``: ``resend``, ``sendgrid``, ``smtp``
or ``console`` (default — renders the message into the log so local development
never needs credentials).
"""

from __future__ import annotations

import json
import logging
import smtplib
import urllib.request
from email.message import EmailMessage
from typing import Any

from apps.api.app.config import get_settings

logger = logging.getLogger("shc.mailer")

_SENT: list[dict[str, Any]] = []
_SENT_MAX = 50


def outbox() -> list[dict[str, Any]]:
    """Recent deliveries, newest first — used by the admin dashboard."""
    return list(reversed(_SENT))


def _record(to: str, subject: str, provider: str, ok: bool, detail: str = "") -> None:
    _SENT.append({"to": to, "subject": subject, "provider": provider, "ok": ok, "detail": detail})
    while len(_SENT) > _SENT_MAX:
        _SENT.pop(0)


def _post(url: str, payload: dict[str, Any], headers: dict[str, str]) -> None:
    request = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers)
    with urllib.request.urlopen(request, timeout=15) as response:
        response.read()


def _send_resend(to: str, subject: str, html: str, text: str) -> None:
    settings = get_settings()
    _post(
        "https://api.resend.com/emails",
        {"from": settings.email_from, "to": [to], "subject": subject, "html": html, "text": text},
        {"Authorization": f"Bearer {settings.email_api_key}", "Content-Type": "application/json"},
    )


def _send_sendgrid(to: str, subject: str, html: str, text: str) -> None:
    settings = get_settings()
    sender = settings.email_from
    if "<" in sender:
        name, address = sender.split("<", 1)
        from_field = {"email": address.rstrip(">").strip(), "name": name.strip()}
    else:
        from_field = {"email": sender}
    _post(
        "https://api.sendgrid.com/v3/mail/send",
        {
            "personalizations": [{"to": [{"email": to}]}],
            "from": from_field,
            "subject": subject,
            "content": [{"type": "text/plain", "value": text}, {"type": "text/html", "value": html}],
        },
        {"Authorization": f"Bearer {settings.email_api_key}", "Content-Type": "application/json"},
    )


def _send_smtp(to: str, subject: str, html: str, text: str) -> None:
    settings = get_settings()
    message = EmailMessage()
    message["From"] = settings.email_from
    message["To"] = to
    message["Subject"] = subject
    if settings.email_reply_to:
        message["Reply-To"] = settings.email_reply_to
    message.set_content(text)
    message.add_alternative(html, subtype="html")
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=20) as server:
        server.starttls()
        if settings.smtp_user:
            server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(message)


def send_email(to: str, subject: str, html: str, text: str) -> dict[str, Any]:
    provider = get_settings().email_provider.lower()
    try:
        if provider == "resend":
            _send_resend(to, subject, html, text)
        elif provider == "sendgrid":
            _send_sendgrid(to, subject, html, text)
        elif provider == "smtp":
            _send_smtp(to, subject, html, text)
        else:
            provider = "console"
            logger.info("[email:%s] %s\n%s", to, subject, text)
        _record(to, subject, provider, True)
        return {"ok": True, "provider": provider}
    except Exception as exc:  # noqa: BLE001
        logger.warning("email delivery failed (%s): %s", provider, exc)
        _record(to, subject, provider, False, str(exc))
        return {"ok": False, "provider": provider, "error": str(exc)}


# ------------------------------------------------------------------ templates

_SHELL = """<!doctype html><html dir="{dir}"><body style="margin:0;background:#05070a;padding:32px 0;
font-family:'IBM Plex Sans','Helvetica Neue',Arial,sans-serif;color:#e8edf4">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center">
<table role="presentation" width="560" cellpadding="0" cellspacing="0"
 style="background:#0d131a;border:1px solid #1e2630;border-radius:14px;overflow:hidden">
<tr><td style="padding:22px 28px;border-bottom:1px solid #1e2630">
  <span style="display:inline-block;width:34px;height:34px;line-height:34px;text-align:center;
   border:1px solid #c8a45a;color:#c8a45a;border-radius:8px;font-weight:700;letter-spacing:.06em">SHC</span>
  <span style="margin:0 10px;font-weight:700;letter-spacing:.14em;color:#c8a45a">SHC</span>
</td></tr>
<tr><td style="padding:26px 28px">{body}</td></tr>
<tr><td style="padding:18px 28px;border-top:1px solid #1e2630;color:#8b98a8;font-size:12px">
  Sovereign Hedge Console · {base}
</td></tr></table></td></tr></table></body></html>"""


def _wrap(body: str, locale: str) -> str:
    return _SHELL.format(
        dir="rtl" if locale == "ar" else "ltr",
        body=body,
        base=get_settings().public_base_url,
    )


def _button(label: str, url: str) -> str:
    return (
        f'<p style="margin:22px 0"><a href="{url}" style="background:#c8a45a;color:#111;padding:12px 20px;'
        f'border-radius:8px;text-decoration:none;font-weight:600">{label}</a></p>'
    )


def send_welcome(email: str, display_name: str, locale: str, verify_url: str) -> dict[str, Any]:
    if locale == "ar":
        subject = "مرحباً بك في SHC — فعّل حسابك"
        body = (
            f"<h2 style='margin:0 0 12px;color:#e8c36a'>مرحباً {display_name}</h2>"
            "<p style='line-height:1.9;color:#c9d2dd'>حسابك في منصة SHC جاهز. المنصة تمنحك الشارت الحي،"
            " مؤشر بصمة الهدوء والاحتقان (VRCS)، «العقل» لتوافق الفريمات، و«الصياد» الذي يرصد الفرص"
            " بنسبة ثقة 90%+ مع تنبيه صوتي ومرئي فوري.</p>"
            "<p style='line-height:1.9;color:#c9d2dd'>فعّل بريدك لتأكيد التسجيل:</p>"
            + _button("تفعيل الحساب", verify_url)
            + "<p style='color:#8b98a8;font-size:12px'>إذا لم تطلب هذا الحساب فتجاهل الرسالة.</p>"
        )
        text = f"مرحباً {display_name}\nفعّل حسابك في SHC: {verify_url}"
    else:
        subject = "Welcome to SHC — activate your account"
        body = (
            f"<h2 style='margin:0 0 12px;color:#e8c36a'>Welcome {display_name}</h2>"
            "<p style='line-height:1.9;color:#c9d2dd'>Your SHC desk is ready: live charts, the VRCS"
            " quiet-compression fingerprint, the Brain for multi-timeframe confluence and the Hunter"
            " that alerts you the moment a 90%+ setup fires.</p>"
            + _button("Activate account", verify_url)
            + "<p style='color:#8b98a8;font-size:12px'>If you did not sign up, ignore this email.</p>"
        )
        text = f"Welcome {display_name}\nActivate your SHC account: {verify_url}"
    return send_email(email, subject, _wrap(body, locale), text)


def send_verified(email: str, display_name: str, locale: str) -> dict[str, Any]:
    if locale == "ar":
        subject = "تم تفعيل حسابك في SHC"
        body = (
            f"<h2 style='margin:0 0 12px;color:#e8c36a'>تم التفعيل</h2>"
            f"<p style='line-height:1.9;color:#c9d2dd'>حسابك {display_name} مفعّل الآن ويمكنك الدخول"
            " إلى المحطة واستخدام الصياد والعقل.</p>" + _button("افتح المحطة", get_settings().public_base_url)
        )
        text = "تم تفعيل حسابك في SHC."
    else:
        subject = "Your SHC account is active"
        body = (
            "<h2 style='margin:0 0 12px;color:#e8c36a'>Activated</h2>"
            f"<p style='line-height:1.9;color:#c9d2dd'>{display_name}, your account is verified. The"
            " terminal, Hunter and Brain are unlocked.</p>" + _button("Open terminal", get_settings().public_base_url)
        )
        text = "Your SHC account is verified."
    return send_email(email, subject, _wrap(body, locale), text)


def send_subscription(email: str, display_name: str, locale: str, plan: str, expires: str) -> dict[str, Any]:
    if locale == "ar":
        subject = f"تأكيد اشتراك SHC — باقة {plan}"
        body = (
            "<h2 style='margin:0 0 12px;color:#e8c36a'>تم تفعيل الاشتراك</h2>"
            f"<p style='line-height:1.9;color:#c9d2dd'>{display_name}، باقتك الحالية <b>{plan}</b>"
            f" وصلاحيتها حتى <b>{expires}</b>.</p>"
        )
        text = f"تم تفعيل باقة {plan} حتى {expires}."
    else:
        subject = f"SHC subscription confirmed — {plan}"
        body = (
            "<h2 style='margin:0 0 12px;color:#e8c36a'>Subscription active</h2>"
            f"<p style='line-height:1.9;color:#c9d2dd'>{display_name}, your plan is <b>{plan}</b>"
            f" valid until <b>{expires}</b>.</p>"
        )
        text = f"Plan {plan} active until {expires}."
    return send_email(email, subject, _wrap(body, locale), text)


def send_reset(email: str, display_name: str, locale: str, reset_url: str) -> dict[str, Any]:
    if locale == "ar":
        subject = "استعادة كلمة مرور SHC"
        body = (
            f"<h2 style='margin:0 0 12px;color:#e8c36a'>إعادة تعيين كلمة المرور</h2>"
            f"<p style='line-height:1.9;color:#c9d2dd'>{display_name}، وصلك هذا الرابط لأن أحداً طلب"
            " استعادة كلمة المرور. الرابط صالح لساعة واحدة:</p>"
            + _button("تعيين كلمة مرور جديدة", reset_url)
            + "<p style='color:#8b98a8;font-size:12px'>إذا لم تطلب الاستعادة فتجاهل الرسالة.</p>"
        )
        text = f"إعادة تعيين كلمة مرور SHC: {reset_url}"
    else:
        subject = "Reset your SHC password"
        body = (
            "<h2 style='margin:0 0 12px;color:#e8c36a'>Password reset</h2>"
            f"<p style='line-height:1.9;color:#c9d2dd'>{display_name}, use this link within one hour"
            " to choose a new password:</p>"
            + _button("Set a new password", reset_url)
            + "<p style='color:#8b98a8;font-size:12px'>If you did not ask for a reset, ignore this email.</p>"
        )
        text = f"Reset your SHC password: {reset_url}"
    return send_email(email, subject, _wrap(body, locale), text)


def send_alert(email: str, display_name: str, locale: str, payload: dict[str, Any]) -> dict[str, Any]:
    symbol = payload.get("symbol") or "—"
    confidence = payload.get("confidence") or "—"
    if locale == "ar":
        subject = f"تنبيه SHC · {symbol} · {confidence}%"
        body = (
            f"<h2 style='margin:0 0 12px;color:#e8c36a'>إشارة نخبة</h2>"
            f"<p style='line-height:1.9;color:#c9d2dd'>{display_name}، {symbol} على {payload.get('timeframe')} "
            f"بنسبة ثقة {confidence}% ({payload.get('side')})</p>"
        )
        text = f"SHC {symbol} {confidence}% {payload.get('side')}"
    else:
        subject = f"SHC alert · {symbol} · {confidence}%"
        body = (
            f"<h2 style='margin:0 0 12px;color:#e8c36a'>Elite signal</h2>"
            f"<p style='line-height:1.9;color:#c9d2dd'>{display_name}, {symbol} on {payload.get('timeframe')} "
            f"at {confidence}% ({payload.get('side')})</p>"
        )
        text = f"SHC {symbol} {confidence}% {payload.get('side')}"
    return send_email(email, subject, _wrap(body, locale), text)
