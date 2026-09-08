import { useEffect, useRef } from "react";
import { createChart, ColorType, type IChartApi, type ISeriesApi, type UTCTimestamp } from "lightweight-charts";
import type { Candle } from "../api";

export function PriceChart({ candles }: { candles: Candle[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const candleRef = useRef<ISeriesApi<"Candlestick"> | null>(null);
  const emaRef = useRef<ISeriesApi<"Line"> | null>(null);

  useEffect(() => {
    if (!ref.current) return;
    const chart = createChart(ref.current, {
      layout: {
        background: { type: ColorType.Solid, color: "#07090d" },
        textColor: "#8b98a8",
        fontFamily: "IBM Plex Sans",
      },
      grid: {
        vertLines: { color: "#151b22" },
        horzLines: { color: "#151b22" },
      },
      rightPriceScale: { borderColor: "#1e2630" },
      timeScale: { borderColor: "#1e2630", timeVisible: true },
      width: ref.current.clientWidth,
      height: ref.current.clientHeight || 460,
    });
    const series = chart.addCandlestickSeries({
      upColor: "#26a69a",
      downColor: "#ef5350",
      borderVisible: false,
      wickUpColor: "#26a69a",
      wickDownColor: "#ef5350",
    });
    const ema = chart.addLineSeries({ color: "#c8a45a", lineWidth: 2 });
    chartRef.current = chart;
    candleRef.current = series;
    emaRef.current = ema;

    const onResize = () => {
      if (!ref.current) return;
      chart.applyOptions({ width: ref.current.clientWidth, height: ref.current.clientHeight || 460 });
    };
    window.addEventListener("resize", onResize);
    return () => {
      window.removeEventListener("resize", onResize);
      chart.remove();
    };
  }, []);

  useEffect(() => {
    if (!candleRef.current || !emaRef.current || candles.length === 0) return;
    const data = candles.map((c) => ({
      time: c.time as UTCTimestamp,
      open: c.open,
      high: c.high,
      low: c.low,
      close: c.close,
    }));
    candleRef.current.setData(data);
    const ema = ema12(candles.map((c) => c.close));
    emaRef.current.setData(
      candles
        .map((c, i) => (ema[i] == null ? null : { time: c.time as UTCTimestamp, value: ema[i] as number }))
        .filter((x): x is { time: UTCTimestamp; value: number } => x !== null),
    );
    chartRef.current?.timeScale().fitContent();
  }, [candles]);

  return <div className="chart-canvas" ref={ref} />;
}

function ema12(values: number[]) {
  const k = 2 / (12 + 1);
  const out: Array<number | null> = [];
  let prev: number | null = null;
  values.forEach((v, i) => {
    if (i < 11) {
      out.push(null);
      return;
    }
    if (prev == null) {
      prev = values.slice(0, 12).reduce((a, b) => a + b, 0) / 12;
    } else {
      prev = v * k + prev * (1 - k);
    }
    out.push(prev);
  });
  return out;
}
