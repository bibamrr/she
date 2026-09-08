import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import ar from "./locales/ar.json";
import en from "./locales/en.json";

const saved = localStorage.getItem("shc_locale") || "ar";

void i18n.use(initReactI18next).init({
  resources: { ar: { translation: ar }, en: { translation: en } },
  lng: saved,
  fallbackLng: "en",
  interpolation: { escapeValue: false },
});

export function applyDocumentDirection(locale: string) {
  document.documentElement.lang = locale;
  document.documentElement.dir = locale === "ar" ? "rtl" : "ltr";
}

applyDocumentDirection(saved);

export default i18n;
