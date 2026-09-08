import { Navigate, Route, Routes } from "react-router-dom";
import { Layout } from "./components/Layout";
import { TerminalPage } from "./pages/Terminal";
import { LoginPage } from "./pages/Login";
import { RegisterPage } from "./pages/Register";
import { BillingPage } from "./pages/Billing";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<TerminalPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/billing" element={<BillingPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
