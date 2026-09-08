import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "../api";
import { useAuth } from "../auth";
import { TopBar } from "../components/TopBar";

export function PlansPage() {
  const { t } = useTranslation();
  const { user, refresh } = useAuth();
  const [plans, setPlans] = useState<{ id: string; price: number; features: string[]; balance_credit: number }[]>([]);
  const [msg, setMsg] = useState("");

  useEffect(() => {
    void api.plans().then((d) => setPlans(d.plans));
  }, []);

  const subscribe = async (id: string) => {
    setMsg("");
    try {
      await api.subscribe(id);
      await refresh();
      setMsg(id);
    } catch (e) {
      setMsg(e instanceof Error ? e.message : "error");
    }
  };

  return (
    <div className="app-shell">
      <TopBar />
      <div className="plans">
        {plans.map((p) => (
          <article key={p.id} className={`plan-card ${user?.plan === p.id ? "active" : ""}`} style={{ display: "block" }}>
            <h2>{t(p.id)}</h2>
            <p>${p.price}</p>
            <ul>
              {p.features.map((f) => (
                <li key={f}>{f}</li>
              ))}
            </ul>
            <button className="primary" disabled={!user} onClick={() => void subscribe(p.id)}>
              {t("subscribe")}
            </button>
          </article>
        ))}
      </div>
      {msg && <p style={{ padding: 16, color: "var(--muted)" }}>{msg}</p>}
      {!user && <p style={{ padding: 16 }}>{t("needAuth")}</p>}
    </div>
  );
}
