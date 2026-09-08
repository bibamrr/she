import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { api, getToken } from "../lib/api";

type Plan = {
  code: string;
  name_en: string;
  name_ar: string;
  monthly_price: number;
  credits_per_month: number;
};

export function BillingPage() {
  const { t, i18n } = useTranslation();
  const [plans, setPlans] = useState<Plan[]>([]);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    void api.plans().then(setPlans);
  }, []);

  async function activate(code: string) {
    if (!getToken()) {
      setMessage(t("needAuth"));
      return;
    }
    const res = await api.subscribe(code);
    setMessage(`${res.plan} · ${res.credits}`);
  }

  const ar = i18n.language.startsWith("ar");
  return (
    <div>
      <h2 style={{ padding: "24px 24px 0" }}>{t("billing.title")}</h2>
      <div className="plans">
        {plans.map((p) => (
          <div className="card" key={p.code}>
            <h3>{ar ? p.name_ar : p.name_en}</h3>
            <div>${p.monthly_price}/mo</div>
            <div className="muted">
              {t("credits")}: {p.credits_per_month}
            </div>
            <button className="btn primary" type="button" style={{ marginTop: 12 }} onClick={() => activate(p.code)}>
              {t("subscribe")}
            </button>
          </div>
        ))}
      </div>
      {message && <p style={{ padding: "0 24px" }}>{message}</p>}
    </div>
  );
}
