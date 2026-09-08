import { useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { api, type Analysis, type Candle } from "../api";
import { useAuth } from "../auth";
import { AgentPanel } from "../components/AgentPanel";
import { PriceChart } from "../components/PriceChart";
import { TopBar } from "../components/TopBar";

const TFS = ["1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d", "3d", "1w", "1M", "1Y"];

export function TerminalPage() {
  const { t } = useTranslation();
  const { user } = useAuth();
  const [symbols, setSymbols] = useState<{ symbol: string; label: string }[]>([]);
  const [symbol, setSymbol] = useState("BTC/USDT");
  const [timeframe, setTimeframe] = useState("15m");
  const [candles, setCandles] = useState<Candle[]>([]);
  const [tick, setTick] = useState<{ price: number; percentage: number } | null>(null);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    void api.symbols().then((d) => setSymbols(d.symbols));
  }, []);

  useEffect(() => {
    setError("");
    void api
      .ohlcv(symbol, timeframe)
      .then((d) => setCandles(d.candles))
      .catch((e) => setError(e.message));
  }, [symbol, timeframe]);

  useEffect(() => {
    const proto = window.location.protocol === "https:" ? "wss" : "ws";
    const ws = new WebSocket(`${proto}://${window.location.host}/api/ws/market?symbol=${encodeURIComponent(symbol)}`);
    ws.onmessage = (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.price) setTick({ price: msg.price, percentage: msg.percentage });
    };
    return () => ws.close();
  }, [symbol]);

  const pctClass = useMemo(() => {
    if (!tick) return "";
    return tick.percentage >= 0 ? "up" : "down";
  }, [tick]);

  const run = async () => {
    if (!user) {
      setError(t("needAuth"));
      return;
    }
    setLoading(true);
    setError("");
    try {
      setAnalysis(await api.analyze(symbol, timeframe));
    } catch (e) {
      setError(e instanceof Error ? e.message : "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <TopBar />
      <div className="terminal">
        <aside className="panel">
          <h3>{t("markets")}</h3>
          {symbols.map((s) => (
            <button
              key={s.symbol}
              className={`symbol-row ${s.symbol === symbol ? "active" : ""}`}
              onClick={() => setSymbol(s.symbol)}
            >
              <span>{s.symbol}</span>
              <span style={{ color: "var(--muted)" }}>{s.label}</span>
            </button>
          ))}
        </aside>
        <section className="chart-wrap">
          <div className="chart-toolbar">
            <strong>{symbol}</strong>
            <span>{t("timeframe")}</span>
            {TFS.map((tf) => (
              <button key={tf} className={tf === timeframe ? "primary" : "ghost"} onClick={() => setTimeframe(tf)}>
                {tf}
              </button>
            ))}
          </div>
          <PriceChart candles={candles} />
          <div className="ticker">
            {t("live")}: <span className={pctClass}>{tick?.price ?? "—"}</span>
            {tick && <span className={pctClass}> ({tick.percentage?.toFixed(2)}%)</span>}
            {error && <span className="down"> · {error}</span>}
          </div>
        </section>
        <AgentPanel analysis={analysis} loading={loading} onRun={() => void run()} />
      </div>
    </div>
  );
}
