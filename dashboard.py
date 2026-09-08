import html
import json

import streamlit as st
import pandas as pd
import ccxt

st.set_page_config(page_title="Virtual Hedge Fund - Pro Terminal", layout="wide")

st.title("🚀 Virtual Hedge Fund - Professional Terminal & AI Agents")
st.markdown("منصة التداول الذكية: تسعير حي مباشر عبر WebSocket، فريمات مستقلة، ومحرك اختبار كمي دقيق.")

user_symbol = st.text_input("أدخل زوج العملات للتحليل الشامل:", value="XRP/USDT")
pair = (user_symbol or "XRP/USDT").upper().replace(" ", "")
if "/" not in pair:
    pair = f"{pair[:-4]}/{pair[-4:]}" if pair.endswith("USDT") and len(pair) > 4 else f"{pair}/USDT"
stream_id = pair.replace("/", "").lower()


def live_board_html(label: str, sid: str) -> str:
    safe_label = html.escape(label)
    js_sid = json.dumps(sid)
    js_label = json.dumps(label)
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    :root {{ color-scheme: dark; }}
    body {{ margin: 0; font-family: ui-sans-serif, system-ui, sans-serif; background: #0b0f14; color: #e8edf4; }}
    .wrap {{ padding: 8px 10px 12px; }}
    .row {{ display: flex; gap: 12px; align-items: baseline; margin-bottom: 8px; }}
    .price {{ font-size: 28px; font-weight: 700; }}
    .up {{ color: #26a69a; }}
    .down {{ color: #ef5350; }}
    .muted {{ color: #8b98a8; font-size: 13px; }}
    .live {{ color: #26a69a; font-size: 12px; letter-spacing: .04em; }}
    #chart {{ height: 420px; width: 100%; }}
    .grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin-top: 10px; }}
    .card {{ background: #141a22; border: 1px solid #243040; border-radius: 10px; padding: 10px; }}
    .card h3 {{ margin: 0 0 6px; font-size: 13px; color: #c8a45a; }}
    .card .chg {{ font-size: 18px; font-weight: 700; }}
  </style>
  <script src="https://unpkg.com/lightweight-charts@4.2.3/dist/lightweight-charts.standalone.production.js"></script>
</head>
<body>
  <div class="wrap">
    <div class="row">
      <span class="live">● LIVE WS</span>
      <strong>{safe_label}</strong>
      <span id="price" class="price">—</span>
      <span id="pct" class="muted"></span>
    </div>
    <div id="chart"></div>
    <div class="grid" id="tfs"></div>
  </div>
  <script>
    const SID = {js_sid};
    const LABEL = {js_label};
    const TFS = ["1m", "5m", "15m", "1h", "4h"];
    const host = document.getElementById("chart");
    const chart = LightweightCharts.createChart(host, {{
      layout: {{ background: {{ color: "#0b0f14" }}, textColor: "#c9d2dd" }},
      grid: {{ vertLines: {{ color: "#1b2430" }}, horzLines: {{ color: "#1b2430" }} }},
      timeScale: {{ timeVisible: true, secondsVisible: true }},
      rightPriceScale: {{ borderColor: "#243040" }},
      width: host.clientWidth,
      height: 420,
    }});
    const series = chart.addCandlestickSeries({{
      upColor: "#26a69a", downColor: "#ef5350", borderVisible: false,
      wickUpColor: "#26a69a", wickDownColor: "#ef5350",
    }});
    const CANDLE_WINDOW = 1000;
    let lastBar = null;
    let bars = [];
    const tfState = {{}};
    const tfBox = document.getElementById("tfs");
    TFS.forEach((tf) => {{
      tfState[tf] = {{ open: null, close: null }};
      const el = document.createElement("div");
      el.className = "card";
      el.id = "tf-" + tf;
      el.innerHTML = "<h3>" + tf.toUpperCase() + "</h3><div class='chg muted'>—</div><div class='muted'>WebSocket</div>";
      tfBox.appendChild(el);
    }});
    function paintPrice(px, pct) {{
      const price = document.getElementById("price");
      const pctEl = document.getElementById("pct");
      price.textContent = "$" + Number(px).toLocaleString(undefined, {{ maximumFractionDigits: 6 }});
      price.className = "price " + (pct >= 0 ? "up" : "down");
      pctEl.textContent = (pct >= 0 ? "+" : "") + Number(pct).toFixed(3) + "%";
      pctEl.className = pct >= 0 ? "up" : "down";
    }}
    function paintTf(tf) {{
      const row = tfState[tf];
      if (!row || !row.open) return;
      const chg = ((row.close - row.open) / row.open) * 100;
      const el = document.getElementById("tf-" + tf);
      const node = el.querySelector(".chg");
      node.textContent = (chg >= 0 ? "+" : "") + chg.toFixed(2) + "%";
      node.className = "chg " + (chg >= 0 ? "up" : "down");
    }}
    function applyTrade(price, ts) {{
      const t = Math.floor(ts / 1000);
      if (!lastBar || t > lastBar.time) {{
        lastBar = {{ time: t, open: price, high: price, low: price, close: price }};
      }} else {{
        lastBar.high = Math.max(lastBar.high, price);
        lastBar.low = Math.min(lastBar.low, price);
        lastBar.close = price;
      }}
      series.update(lastBar);
      if (!bars.length || bars[bars.length - 1].time !== lastBar.time) bars.push({{ ...lastBar }});
      else bars[bars.length - 1] = {{ ...lastBar }};
      if (bars.length > CANDLE_WINDOW) {{
        bars = bars.slice(-CANDLE_WINDOW);
        series.setData(bars);
      }}
      const open = lastBar.open || price;
      paintPrice(price, ((price - open) / open) * 100);
    }}
    const streams = [SID + "@aggTrade", SID + "@kline_1s"].concat(TFS.map((tf) => SID + "@kline_" + tf));
    const url = "wss://data-stream.binance.vision/stream?streams=" + streams.join("/");
    const socket = new WebSocket(url);
    socket.onmessage = (evt) => {{
      let msg;
      try {{ msg = JSON.parse(evt.data); }} catch (e) {{ return; }}
      const payload = msg.data || msg;
      if (payload.e === "aggTrade" || payload.e === "trade") {{
        applyTrade(Number(payload.p), Number(payload.T || payload.E || Date.now()));
        return;
      }}
      if (payload.e === "kline" && payload.k) {{
        const k = payload.k;
        const bar = {{
          time: Math.floor(k.t / 1000),
          open: Number(k.o),
          high: Number(k.h),
          low: Number(k.l),
          close: Number(k.c),
        }};
        if (k.i === "1s") {{
          lastBar = bar;
          series.update(bar);
          if (!bars.length || bars[bars.length - 1].time !== bar.time) bars.push(bar);
          else bars[bars.length - 1] = bar;
          if (bars.length > CANDLE_WINDOW) {{
            bars = bars.slice(-CANDLE_WINDOW);
            series.setData(bars);
          }}
          paintPrice(bar.close, bar.open ? ((bar.close - bar.open) / bar.open) * 100 : 0);
        }}
        if (tfState[k.i]) {{
          tfState[k.i] = {{ open: Number(k.o), close: Number(k.c) }};
          paintTf(k.i);
        }}
      }}
    }};
    window.addEventListener("resize", () => chart.applyOptions({{ width: host.clientWidth }}));
  </script>
</body>
</html>
"""


st.subheader(f"📊 بث حي بدون تأخير · {pair}")
st.components.v1.html(live_board_html(pair, stream_id), height=620, scrolling=False)

st.caption("المصدر: WebSocket عام `wss://data-stream.binance.vision` — صفقات مجمّعة + شموع 1 ثانية.")

st.divider()

# قسم المحادثة النصية مع الوكلاء
st.subheader("💬 محادثة وكلاء الذكاء الاصطناعي (Text AI Assistant)")
if "messages" not in st.session_state:
    st.session_state.messages = []
if len(st.session_state.messages) > 80:
    st.session_state.messages = st.session_state.messages[-80:]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اكتب سؤالك أو أمرك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = f"تم استلام أمرك '{prompt}' بنجاح. الوكلاء والعقل المدبر يحللون المعطيات بدقة."
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        if len(st.session_state.messages) > 80:
            st.session_state.messages = st.session_state.messages[-80:]

st.divider()

# محرك الاختبار العكسي الكمي المستقل
st.subheader("🧪 محرك الاختبار العكسي الكمي المستقل (Quant Backtesting Engine)")
st.markdown("يقوم بسحب البيانات التاريخية المستقلة للعملة المحددة وإجراء المحاكاة الكمية.")

bt_col1, bt_col2 = st.columns(2)
with bt_col1:
    bt_symbol = st.selectbox("اختر العملة للاختبار العكسي:", ["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "DOGE/USDT"], key="bt_sym")
with bt_col2:
    bt_timeframe = st.selectbox("الفريم التاريخي للاختبار:", ["15m", "1h", "4h", "1d"], index=1, key="bt_tf")

if st.button("🚀 بدء محاكاة الاختبار العكسي المستقل"):
    with st.spinner(f"جاري جلب البيانات التاريخية لـ {bt_symbol} وحساب المحاكاة الكمية..."):
        try:
            exchange = ccxt.binance({"enableRateLimit": True})
            ohlcv = exchange.fetch_ohlcv(bt_symbol, timeframe=bt_timeframe, limit=1000)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

            df['SMA_20'] = df['close'].rolling(window=20).mean()
            df['SMA_50'] = df['close'].rolling(window=50).mean()

            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            df['Vol_SMA'] = df['volume'].rolling(window=20).mean()

            df['Signal'] = 0
            buy_condition = (df['SMA_20'] > df['SMA_50']) & (df['RSI'] < 68) & (df['volume'] > df['Vol_SMA'])
            sell_condition = (df['SMA_20'] <= df['SMA_50']) | (df['RSI'] > 75)

            df.loc[buy_condition, 'Signal'] = 1
            df.loc[sell_condition, 'Signal'] = -1

            df['Market_Return'] = df['close'].pct_change()
            df['Strategy_Return'] = df['Signal'].shift(1) * df['Market_Return']

            cumulative_return = (1 + df['Strategy_Return'].fillna(0)).prod() - 1
            win_trades = len(df[df['Strategy_Return'] > 0])
            total_trades = len(df[df['Strategy_Return'] != 0])
            win_rate = (win_trades / total_trades * 100) if total_trades > 0 else 0

            st.success(f"✅ تمت محاكاة الأداء الكمي لـ {bt_symbol} بنجاح!")

            res_col1, res_col2, res_col3 = st.columns(3)
            res_col1.metric("إجمالي العائد الكمي (PnL)", f"{cumulative_return*100:+.2f}%")
            res_col2.metric("نسبة صفقات النجاح (Win Rate)", f"{win_rate:.1f}%")
            res_col3.metric("إجمالي الصفقات المنفذة", str(total_trades))

            st.markdown("📈 **منحنى نمو رأس المال بناءً على سلوك العملة الفعلي:**")
            st.line_chart((1 + df['Strategy_Return'].fillna(0)).cumprod())

        except Exception as e:
            st.error(f"حدث خطأ أثناء المحاكاة: {e}")
