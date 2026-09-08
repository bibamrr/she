import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { api, setToken } from "../lib/api";
import i18n from "../i18n";

export function RegisterPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    try {
      const res = await api.register({
        email,
        password,
        display_name: name || "Trader",
        preferred_locale: i18n.language.startsWith("ar") ? "ar" : "en",
      });
      setToken(res.access_token);
      navigate("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "error");
    }
  }

  return (
    <form className="auth-page" onSubmit={onSubmit}>
      <h2>{t("register.title")}</h2>
      <label>{t("name")}</label>
      <input value={name} onChange={(e) => setName(e.target.value)} />
      <label>{t("email")}</label>
      <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required />
      <label>{t("password")}</label>
      <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" minLength={8} required />
      {error && <div className="err">{error}</div>}
      <button className="btn primary" type="submit" style={{ marginTop: 16, width: "100%" }}>
        {t("submit")}
      </button>
    </form>
  );
}
