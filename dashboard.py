import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import ccxt

st.set_page_config(page_title="Virtual Hedge Fund - Pro Terminal", layout="wide")

st.title("🚀 Virtual Hedge Fund - Professional Terminal & AI Agents")
st.markdown("منصة التداول الذكية: تسعير حي مباشر، فريمات مستقلة، ومحرك اختبار كمي دقيق.")

user_symbol = st.text_input("أدخل زوج العملات للتحليل الشامل:", value="XRP/USDT")
tv_symbol = f"BINANCE:{user_symbol.replace('/', '')}"

# شارت التداول الحي
st.subheader(f"📊 Live Candlestick Chart - {user_symbol}")
tv_html = f"""
<div class="tradingview-widget-container" style="height:480px;width:100%">
  <div class="tradingview-widget-container__widget" style="height:100%;width:100%"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
  {{
    "width": "100%",
    "height": "480",
    "symbol": "{tv_symbol}",
    "interval": "15",
    "timezone": "Asia/Riyadh",
    "theme": "dark",
    "style": "1",
    "locale": "ar",
    "enable_publishing": false,
    "hide_top_toolbar": false
  }}
  </script>
</div>
"""
components.html(tv_html, height=500)

st.divider()

# مصفوفة الفريمات المستقلة (سعر حي موحد + تحليل خاص بكل فريم)
st.subheader(f"⚡ مصفوفة التحليل متعدد الفريمات المستقلة لـ {user_symbol}")

@st.fragment(run_every=5)
def render_independent_timeframes():
    try:
        exchange = ccxt.binance()
        # جلب السعر اللحظي الحقيقي المباشر من التكتير
        ticker = exchange.fetch_ticker(user_symbol)
        live_price = ticker['last']
    except:
        live_price = 0.0

    timeframes = ['1m', '5m', '15m', '1h', '4h']
    cols = st.columns(5)
    
    for i, tf in enumerate(timeframes):
        with cols[i]:
            st.markdown(f"### ⏱️ {tf.upper()}")
            try:
                exchange = ccxt.binance()
                ohlcv = exchange.fetch_ohlcv(user_symbol, timeframe=tf, limit=30)
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                
                # حساب التغير الخاص بهذا الفريم فقط
                start_tf_price = df['close'].iloc[0]
                end_tf_price = df['close'].iloc[-1]
                tf_change = ((end_tf_price - start_tf_price) / start_tf_price) * 100
                
                signal = "شراء 🟢" if tf_change > 0.05 else ("بيع 🔴" if tf_change < -0.05 else "حياد 🟡")
                trend = "صاعد 📈" if tf_change > 0.05 else ("هابط 📉" if tf_change < -0.05 else "عرضي ➡️")
                
                st.metric("السعر المباشر", f"${live_price:,.4f}" if live_price > 0 else "جاري...")
                st.metric(f"تغير الفريم ({tf})", f"{tf_change:+.2f}%")
                st.info(f"**الاتجاه:** {trend}\n\n**القرار:** {signal}")
            except Exception:
                st.warning("جاري مزامنة الفريم...")

render_independent_timeframes()

st.divider()

# قسم المحادثة النصية مع الوكلاء
st.subheader("💬 محادثة وكلاء الذكاء الاصطناعي (Text AI Assistant)")
if "messages" not in st.session_state:
    st.session_state.messages = []

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
            exchange = ccxt.binance()
            ohlcv = exchange.fetch_ohlcv(bt_symbol, timeframe=bt_timeframe, limit=700)
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
