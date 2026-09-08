import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./auth";
import { LoginPage } from "./pages/LoginPage";
import { PlansPage } from "./pages/PlansPage";
import { TerminalPage } from "./pages/TerminalPage";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<TerminalPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/plans" element={<PlansPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
