const TOKEN_KEY = "shc-token";

export function getToken(): string | null {
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
      detail = body.detail || detail;
    } catch {
      /* ignore */
    }
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return res.json() as Promise<T>;
}

export type Ticker = {
  symbol: string;
  last: number;
  percentage: number;
  bid: number;
  ask: number;
  high: number;
  low: number;
  timestamp_ms: number;
};

export type Candle = {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
};

export type UserMe = {
  email: string;
  display_name: string;
  preferred_locale: string;
  plan: string;
  balance: number;
  credits: number;
};

export type AgentResult = {
  symbol: string;
  timeframe: string;
  credits_remaining: number;
  last_close: number;
  opinions: Array<{
    source: string;
    direction: string;
    confidence: number;
    win_probability: number;
    reasoning_en: string;
    reasoning_ar: string;
    suggested_entry: number | null;
    suggested_stop_loss: number | null;
  }>;
  consensus: {
    direction: string;
    confidence: number;
    win_probability: number;
    entry: number | null;
    stop_loss: number | null;
    reasoning_en: string;
    reasoning_ar: string;
  };
};

export const api = {
  health: () => request<{ ok: boolean }>("/health"),
  watchlist: () => request<{ symbols: string[] }>("/api/market/watchlist"),
  ticker: (symbol: string) => request<Ticker>(`/api/market/ticker?symbol=${encodeURIComponent(symbol)}`),
  ohlcv: (symbol: string, timeframe: string) =>
    request<{ candles: Candle[] }>(
      `/api/market/ohlcv?symbol=${encodeURIComponent(symbol)}&timeframe=${timeframe}&limit=400`,
    ),
  orderbook: (symbol: string) =>
    request<{ bids: { price: number; amount: number }[]; asks: { price: number; amount: number }[] }>(
      `/api/market/orderbook?symbol=${encodeURIComponent(symbol)}`,
    ),
  register: (body: { email: string; password: string; display_name: string; preferred_locale: string }) =>
    request<{ access_token: string }>("/api/auth/register", { method: "POST", body: JSON.stringify(body) }),
  login: (email: string, password: string) =>
    request<{ access_token: string }>("/api/auth/login-json", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  me: () => request<UserMe>("/api/auth/me"),
  plans: () =>
    request<
      Array<{
        code: string;
        name_en: string;
        name_ar: string;
        monthly_price: number;
        credits_per_month: number;
      }>
    >("/api/billing/plans"),
  subscribe: (plan: string) =>
    request<{ plan: string; credits: number }>("/api/billing/subscribe", {
      method: "POST",
      body: JSON.stringify({ plan, deposit: 0 }),
    }),
  analyze: (symbol: string, timeframe: string) =>
    request<AgentResult>(
      `/api/agents/analyze?symbol=${encodeURIComponent(symbol)}&timeframe=${timeframe}`,
      { method: "POST" },
    ),
};
