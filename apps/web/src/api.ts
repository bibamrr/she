const TOKEN_KEY = "shc_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string | null) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set("Content-Type", "application/json");
  const token = getToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const res = await fetch(path, { ...init, headers });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail || JSON.stringify(body);
    } catch {
      /* ignore */
    }
    throw new Error(detail);
  }
  return res.json() as Promise<T>;
}

export type User = {
  id: number;
  email: string;
  display_name: string;
  locale: string;
  plan: string;
  balance: number;
};

export type Candle = {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume?: number;
};

export type AgentView = {
  name: string;
  direction: string;
  confidence: number;
  reasoning: string;
  metrics?: Record<string, unknown>;
};

export type Analysis = {
  symbol: string;
  timeframe: string;
  last_price: number;
  direction: string;
  success_probability: number;
  entry?: number;
  stop_loss?: number | null;
  take_profits?: number[];
  reasoning: string;
  agents: AgentView[];
};

export const api = {
  health: () => request<{ ok: boolean }>("/api/health"),
  register: (body: object) => request<{ access_token: string }>("/api/auth/register", { method: "POST", body: JSON.stringify(body) }),
  login: (body: object) => request<{ access_token: string }>("/api/auth/login", { method: "POST", body: JSON.stringify(body) }),
  me: () => request<User>("/api/auth/me"),
  symbols: () => request<{ symbols: { symbol: string; label: string }[] }>("/api/market/symbols"),
  ohlcv: (symbol: string, timeframe: string) =>
    request<{ candles: Candle[] }>(`/api/market/ohlcv?symbol=${encodeURIComponent(symbol)}&timeframe=${timeframe}`),
  compute: (symbol: string, timeframe: string, ids = "vrcs,volume,ema12") =>
    request<Record<string, unknown>>(
      `/api/indicators/compute?symbol=${encodeURIComponent(symbol)}&timeframe=${timeframe}&ids=${ids}`,
    ),
  ticker: (symbol: string) => request<{ last: number; percentage: number }>(`/api/market/ticker?symbol=${encodeURIComponent(symbol)}`),
  analyze: (symbol: string, timeframe: string) =>
    request<Analysis>("/api/agents/analyze", { method: "POST", body: JSON.stringify({ symbol, timeframe }) }),
  plans: () => request<{ plans: { id: string; price: number; features: string[]; balance_credit: number }[] }>("/api/subscriptions/plans"),
  subscribe: (plan: string) => request<User>("/api/subscriptions/subscribe", { method: "POST", body: JSON.stringify({ plan }) }),
};
