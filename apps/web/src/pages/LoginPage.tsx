import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useAuth } from "../auth";
import i18n, { applyDocumentDirection } from "../i18n";

export function LoginPage() {
  const { t } = useTranslation();
  const { login, register } = useAuth();
  const nav = useNavigate();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      if (mode === "login") await login(email, password);
      else await register(email, password, name, i18n.language);
      nav("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error");
    }
  };

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={onSubmit}>
        <div className="brand" style={{ marginBottom: 12 }}>
          <span className="brand-mark">SHC</span>
          <span>{t("brand")}</span>
        </div>
        <h1>{mode === "login" ? t("login") : t("register")}</h1>
        <p>{t("tagline")}</p>
        {mode === "register" && (
          <label className="field">
            {t("name")}
            <input value={name} onChange={(e) => setName(e.target.value)} />
          </label>
        )}
        <label className="field">
          {t("email")}
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label className="field">
          {t("password")}
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required minLength={8} />
        </label>
        {error && <p className="down">{error}</p>}
        <button className="primary" type="submit" style={{ width: "100%" }}>
          {mode === "login" ? t("login") : t("register")}
        </button>
        <p>
          <button
            type="button"
            className="ghost"
            style={{ marginTop: 12 }}
            onClick={() => setMode(mode === "login" ? "register" : "login")}
          >
            {mode === "login" ? t("register") : t("login")}
          </button>
          <button
            type="button"
            className="ghost"
            style={{ marginInlineStart: 8 }}
            onClick={() => {
              const next = i18n.language === "ar" ? "en" : "ar";
              void i18n.changeLanguage(next);
              localStorage.setItem("shc_locale", next);
              applyDocumentDirection(next);
            }}
          >
            {i18n.language === "ar" ? "EN" : "ع"}
          </button>
        </p>
      </form>
    </div>
  );
}
