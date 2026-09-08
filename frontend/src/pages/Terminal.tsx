import { FormEvent, useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { ChartPanel } from "../components/ChartPanel";
import { AgentResult, api, Candle, getToken, UserMe } from "../lib/api";

const TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h", "1d"];

export function TerminalPage() {
  const { t, i18n } = useTranslation();
  const [symbols, setSymbols] = useState<string[]>(["BTC/USDT"]);
  const [symbol, setSymbol] = useState("BTC/USDT");
  const [timeframe, setTimeframe] = useState("1h");
  const [indicator, setIndicator] = useState<"none" | "ema">("ema");
  const [candles, setCandles] = useState<Candle[]>([]);
  const [live, setLive] = useState<number | null>(null);
  const [change, setChange] = useState(0);
  const [book, setBook] = useState<{ bids: { price: number; amount: number }[]; asks: { price: number; amount: number }[] }>({
    bids: [],
    asks: [],
  });
  const [me, setMe] = useState<UserMe | null>(null);
  const [analysis, setAnalysis] = useState<AgentResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    void api.watchlist().then((r) => setSymbols(r.symbols));
    if (getToken()) void api.me().then(setMe).catch(() => setMe(null));
  }, []);

  useEffect(() => {
    setError(null);
    void api.ohlcv(symbol, timeframe).then((r) => setCandles(r.candles)).catch((e) => setError(String(e.message)));
    void api.orderbook(symbol).then(setBook).catch(() => undefined);
  }, [symbol, timeframe]);

  useEffect(() => {
    const ws = new WebSocket(`${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws/ticker?symbol=${encodeURIComponent(symbol)}`);
    ws.onmessage = (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.type === "tick") {
        setLive(msg.last);
        setChange(msg.percentage);
      }
    };
    return () => ws.close();
  }, [symbol]);

  async function runAgents(e: FormEvent) {
    e.preventDefault();
    if (!getToken()) {
      setError(t("needAuth"));
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const result = await api.analyze(symbol, timeframe);
      setAnalysis(result);
      setMe((prev) => (prev ? { ...prev, credits: result.credits_remaining } : prev));
    } catch (err) {
      setError(err instanceof Error ? err.message : "error");
    } finally {
      setLoading(false);
    }
  }

  const locale = i18n.language.startsWith("ar") ? "ar" : "en";
  const pctClass = change >= 0 ? "up" : "down";
  const consensus = analysis?.consensus;
  const reasoning = useMemo(() => {
    if (!analysis) return [];
    return analysis.opinions.map((o) => ({
      ...o,
      text: locale === "ar" ? o.reasoning_ar : o.reasoning_en,
    }));
  }, [analysis, locale]);

  return (
    <div className="terminal">
      <aside className="side">
        <div className="muted">{t("watchlist")}</div>
        {symbols.map((s) => (
          <div key={s} className={`row ${s === symbol ? "active" : ""}`} onClick={() => setSymbol(s)}>
            <span>{s}</span>
          </div>
        ))}
        {me && (
          <div className="card" style={{ marginTop: 16 }}>
            <div className="muted">{me.display_name}</div>
            <div>
              {t("plan")}: {me.plan}
            </div>
            <div>
              {t("credits")}: {me.credits}
            </div>
          </div>
        )}
      </aside>
      <section className="center">
        <div className="toolbar">
          <strong>{symbol}</strong>
          <span className={pctClass}>
            {t("live")}: {live != null ? live.toLocaleString(undefined, { maximumFractionDigits: 4 }) : "—"} ({change.toFixed(2)}%)
          </span>
          <label className="muted" style={{ margin: 0 }}>
            {t("timeframe")}
          </label>
          <select value={timeframe} onChange={(e) => setTimeframe(e.target.value)} style={{ width: 90 }}>
            {TIMEFRAMES.map((tf) => (
              <option key={tf}>{tf}</option>
            ))}
          </select>
          <label className="muted" style={{ margin: 0 }}>
            {t("indicator")}
          </label>
          <select value={indicator} onChange={(e) => setIndicator(e.target.value as "none" | "ema")} style={{ width: 90 }}>
            <option value="ema">EMA 20</option>
            <option value="none">{t("none")}</option>
          </select>
        </div>
        <ChartPanel candles={candles} indicator={indicator} />
        <div className="book">
          <div>
            <div className="muted">{t("bids")}</div>
            {book.bids.slice(0, 8).map((lvl) => (
              <div key={`b${lvl.price}`} className="row">
                <span className="up">{lvl.price}</span>
                <span>{lvl.amount.toFixed(4)}</span>
              </div>
            ))}
          </div>
          <div>
            <div className="muted">{t("asks")}</div>
            {book.asks.slice(0, 8).map((lvl) => (
              <div key={`a${lvl.price}`} className="row">
                <span className="down">{lvl.price}</span>
                <span>{lvl.amount.toFixed(4)}</span>
              </div>
            ))}
          </div>
        </div>
      </section>
      <aside className="agents">
        <div className="muted">{t("agents")}</div>
        <form onSubmit={runAgents}>
          <button className="btn primary" type="submit" disabled={loading} style={{ width: "100%", margin: "10px 0" }}>
            {loading ? "..." : t("runAgents")}
          </button>
        </form>
        {error && <div className="err">{error}</div>}
        {consensus && (
          <div className="card">
            <div className="muted">{t("consensus")}</div>
            <div className={consensus.direction === "bullish" ? "up" : consensus.direction === "bearish" ? "down" : ""}>
              {consensus.direction.toUpperCase()} · {(consensus.win_probability * 100).toFixed(0)}% {t("win")}
            </div>
            <div className="muted">{locale === "ar" ? consensus.reasoning_ar : consensus.reasoning_en}</div>
            {consensus.entry && (
              <div>
                {t("entry")}: {consensus.entry.toFixed(4)} {consensus.stop_loss ? `· ${t("sl")} ${consensus.stop_loss.toFixed(4)}` : ""}
              </div>
            )}
          </div>
        )}
        {reasoning.map((o) => (
          <div className="card" key={o.source}>
            <strong>{o.source}</strong>
            <div className={o.direction === "bullish" ? "up" : o.direction === "bearish" ? "down" : ""}>
              {o.direction} · {(o.win_probability * 100).toFixed(0)}%
            </div>
            <div className="muted">{o.text}</div>
          </div>
        ))}
      </aside>
    </div>
  );
}
