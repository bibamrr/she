import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { api, setToken } from "../lib/api";

export function LoginPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    try {
      const res = await api.login(email, password);
      setToken(res.access_token);
      navigate("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "error");
    }
  }

  return (
    <form className="auth-page" onSubmit={onSubmit}>
      <h2>{t("login.title")}</h2>
      <label>{t("email")}</label>
      <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required />
      <label>{t("password")}</label>
      <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" required />
      {error && <div className="err">{error}</div>}
      <button className="btn primary" type="submit" style={{ marginTop: 16, width: "100%" }}>
        {t("submit")}
      </button>
    </form>
  );
}
