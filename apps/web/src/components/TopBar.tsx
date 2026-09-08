import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useAuth } from "../auth";
import i18n, { applyDocumentDirection } from "../i18n";

export function TopBar() {
  const { t } = useTranslation();
  const { user, logout } = useAuth();

  const toggleLocale = () => {
    const next = i18n.language === "ar" ? "en" : "ar";
    void i18n.changeLanguage(next);
    localStorage.setItem("shc_locale", next);
    applyDocumentDirection(next);
  };

  return (
    <header className="topbar">
      <Link to="/" className="brand">
        <span className="brand-mark">SHC</span>
        <span>{t("brand")}</span>
      </Link>
      <div className="topbar-actions">
        {user && (
          <span style={{ color: "var(--muted)", fontSize: 13 }}>
            {t("plan")}: {user.plan} · {t("balance")}: {user.balance}
          </span>
        )}
        <button className="ghost" onClick={toggleLocale}>
          {i18n.language === "ar" ? "EN" : "ع"}
        </button>
        <Link className="ghost" to="/plans">
          {t("plans")}
        </Link>
        {user ? (
          <button className="ghost" onClick={logout}>
            {t("logout")}
          </button>
        ) : (
          <Link className="primary" to="/login">
            {t("login")}
          </Link>
        )}
      </div>
    </header>
  );
}
