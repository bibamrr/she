import { useTranslation } from "react-i18next";
import type { Analysis } from "../api";

export function AgentPanel({
  analysis,
  loading,
  onRun,
}: {
  analysis: Analysis | null;
  loading: boolean;
  onRun: () => void;
}) {
  const { t } = useTranslation();
  return (
    <aside className="panel">
      <h3>{t("agents")}</h3>
      <div style={{ padding: 12 }}>
        <button className="primary" onClick={onRun} disabled={loading} style={{ width: "100%" }}>
          {loading ? t("analyzing") : t("runAnalysis")}
        </button>
      </div>
      {!analysis && <p style={{ padding: 16, color: "var(--muted)" }}>{t("noResult")}</p>}
      {analysis && (
        <>
          <div className="agent-card">
            <strong>{t("oracle")}</strong>
            <div className={analysis.direction === "bullish" ? "up" : analysis.direction === "bearish" ? "down" : ""}>
              {analysis.direction.toUpperCase()}
            </div>
            <div>
              {t("success")}: {(analysis.success_probability * 100).toFixed(1)}%
            </div>
            {analysis.entry != null && (
              <div>
                {t("entry")}: {analysis.entry} · {t("stop")}: {analysis.stop_loss ?? "—"}
              </div>
            )}
            <p style={{ color: "var(--muted)", fontSize: 13 }}>{analysis.reasoning}</p>
          </div>
          {analysis.agents.map((agent) => (
            <div className="agent-card" key={agent.name}>
              <strong>{agent.name}</strong>
              <div className={agent.direction === "bullish" ? "up" : agent.direction === "bearish" ? "down" : ""}>
                {agent.direction} · {(agent.confidence * 100).toFixed(0)}%
              </div>
              <p style={{ color: "var(--muted)", fontSize: 13 }}>{agent.reasoning}</p>
            </div>
          ))}
        </>
      )}
    </aside>
  );
}
