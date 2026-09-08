import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { getToken, setToken } from "../lib/api";
import i18n, { applyDocumentLocale } from "../i18n";

export function Layout() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const authed = Boolean(getToken());

  function toggleLocale() {
    const next = i18n.language === "ar" ? "en" : "ar";
    void i18n.changeLanguage(next);
    localStorage.setItem("shc-locale", next);
    applyDocumentLocale(next);
  }

  function logout() {
    setToken(null);
    navigate("/login");
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">SH</div>
          <div>
            <div>{t("brand")}</div>
            <div className="muted">{t("tagline")}</div>
          </div>
        </div>
        <nav className="nav">
          <NavLink to="/" end>
            {t("nav.terminal")}
          </NavLink>
          <NavLink to="/billing">{t("nav.billing")}</NavLink>
          <button className="chip" onClick={toggleLocale} type="button">
            {t("lang")}
          </button>
          {authed ? (
            <button className="chip" onClick={logout} type="button">
              {t("nav.logout")}
            </button>
          ) : (
            <>
              <NavLink to="/login">{t("nav.login")}</NavLink>
              <NavLink to="/register">{t("nav.register")}</NavLink>
            </>
          )}
        </nav>
      </header>
      <Outlet />
    </div>
  );
}
