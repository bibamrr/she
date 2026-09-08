import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import ar from "./ar.json";
import en from "./en.json";

const saved = localStorage.getItem("shc-locale") || "ar";

void i18n.use(initReactI18next).init({
  resources: { ar: { translation: ar }, en: { translation: en } },
  lng: saved,
  fallbackLng: "en",
  interpolation: { escapeValue: false },
});

export function applyDocumentLocale(locale: string) {
  document.documentElement.lang = locale;
  document.documentElement.dir = locale === "ar" ? "rtl" : "ltr";
  document.body.style.fontFamily =
    locale === "ar"
      ? '"IBM Plex Sans Arabic", "IBM Plex Sans", system-ui, sans-serif'
      : '"IBM Plex Sans", "IBM Plex Sans Arabic", system-ui, sans-serif';
}

applyDocumentLocale(saved);

export default i18n;
