# SHC — Sovereign Hedge Console

منصة تحليل وتداول: شارت حي، وكلاء كميون، حسابات واشتراكات. الواجهة عربية/إنجليزية (RTL/LTR).

## التشغيل

من جذر المشروع:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# المنصة كاملة (واجهة + API)  →  http://127.0.0.1:8000
PYTHONPATH=. uvicorn apps.api.app.main:app --reload --port 8000

# تطوير React (اختياري إذا كان Node مثبتاً)
cd apps/web && npm install && npm run dev
```

افتح المتصفح على المنفذ 8000، أنشئ حساباً من زر الدخول، ثم شغّل التحليل السربي.

## الهيكل

```
apps/api/          FastAPI: auth, market, scanner, hunter, websocket, subscriptions, agents
apps/web/          واجهة المحطة (static) + مشروع Vite + React
engine/            محرك الوكلاء + VRCS + الثقة + توافق الفريمات + الباك تست
indicators/        EMA / RSI / MACD / ATR + المؤشرات الكلاسيكية
agents/            سرب البث القديم (Radar / Visionary / Sniper)
```

## واجهات "الصياد" و"العقل"

| المسار | الوظيفة |
| --- | --- |
| `GET /api/hunter/scan` | مسح أعلى العملات سيولة وإرجاع المحتقنة/المنفجرة مع نسبة الثقة ومرشح التدفق الحجمي في الشموع الهادئة |
| `GET /api/hunter/confluence` | توافق الاحتقان والاختراق عبر عدة فريمات في وقت واحد |
| `GET /api/hunter/backtest` | سجل الفرص السابقة ونسبة النجاح موزعة على شرائح الثقة |
| `GET /api/hunter/export.csv` | تصدير تقرير الفرص للأرشيف |
| `GET /api/hunter/correlation` | مصفوفة ارتباط العملات بالبيتكوين |
| `GET /api/hunter/heatmap` | ساعات اليوم الأكثر احتقاناً وانفجاراً (UTC) |

بث الأسعار اللحظي يأتي مباشرة من Binance WebSocket في المتصفح (`kline` + `miniTicker`)، مع تخزين مؤقت
ذكي في الواجهة (LRU + TTL) وتنبيه صوتي/مرئي فوري عند أي إشارة بثقة 90%+.

صفحات SPA: `#/` المحطة · `#/history` سجل الفرص · `#/reports` التقارير · `#/settings` الإعدادات.
البريد الترحيبي يعمل عبر `SHC_EMAIL_PROVIDER` (console/resend/sendgrid/smtp).
المعايرة: `GET /api/hunter/calibrate?apply=true` ثم تُطبَّق على نسب الثقة الحية.
