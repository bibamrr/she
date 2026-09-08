import { useEffect, useRef } from "react";
import { ColorType, createChart, IChartApi, ISeriesApi, Time } from "lightweight-charts";
import type { Candle } from "../lib/api";

type Props = {
  candles: Candle[];
  indicator: "none" | "ema";
};

function ema(values: number[], period: number) {
  const k = 2 / (period + 1);
  const out: number[] = [];
  let prev = values[0] ?? 0;
  values.forEach((v, i) => {
    prev = i === 0 ? v : v * k + prev * (1 - k);
    out.push(prev);
  });
  return out;
}

export function ChartPanel({ candles, indicator }: Props) {
  const ref = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const candleSeries = useRef<ISeriesApi<"Candlestick"> | null>(null);
  const volumeSeries = useRef<ISeriesApi<"Histogram"> | null>(null);
  const emaSeries = useRef<ISeriesApi<"Line"> | null>(null);

  useEffect(() => {
    if (!ref.current) return;
    const chart = createChart(ref.current, {
      layout: {
        background: { type: ColorType.Solid, color: "#07090c" },
        textColor: "#8b9bb4",
      },
      grid: {
        vertLines: { color: "#1b2430" },
        horzLines: { color: "#1b2430" },
      },
      rightPriceScale: { borderColor: "#243041" },
      timeScale: { borderColor: "#243041", timeVisible: true },
      autoSize: true,
    });
    const candlesApi = chart.addCandlestickSeries({
      upColor: "#0ecb81",
      downColor: "#f6465d",
      borderVisible: false,
      wickUpColor: "#0ecb81",
      wickDownColor: "#f6465d",
    });
    const volumes = chart.addHistogramSeries({
      priceFormat: { type: "volume" },
      priceScaleId: "vol",
    });
    chart.priceScale("vol").applyOptions({ scaleMargins: { top: 0.8, bottom: 0 } });
    const emaApi = chart.addLineSeries({ color: "#d4a017", lineWidth: 2 });
    chartRef.current = chart;
    candleSeries.current = candlesApi;
    volumeSeries.current = volumes;
    emaSeries.current = emaApi;
    const onResize = () => chart.applyOptions({ autoSize: true });
    window.addEventListener("resize", onResize);
    return () => {
      window.removeEventListener("resize", onResize);
      chart.remove();
    };
  }, []);

  useEffect(() => {
    if (!candleSeries.current || !volumeSeries.current || !emaSeries.current) return;
    const mapped = candles.map((c) => ({
      time: c.time as Time,
      open: c.open,
      high: c.high,
      low: c.low,
      close: c.close,
    }));
    candleSeries.current.setData(mapped);
    volumeSeries.current.setData(
      candles.map((c) => ({
        time: c.time as Time,
        value: c.volume,
        color: c.close >= c.open ? "rgba(14,203,129,0.4)" : "rgba(246,70,93,0.4)",
      })),
    );
    if (indicator === "ema") {
      const values = ema(
        candles.map((c) => c.close),
        20,
      );
      emaSeries.current.setData(candles.map((c, i) => ({ time: c.time as Time, value: values[i] })));
    } else {
      emaSeries.current.setData([]);
    }
  }, [candles, indicator]);

  return <div ref={ref} className="chart-wrap" style={{ height: "100%", width: "100%" }} />;
}
