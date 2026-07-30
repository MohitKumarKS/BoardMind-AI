import { useState, useEffect } from "react";
import "./SessionHistoryPage.css";

interface AgentSummary {
  agent_id: string;
  position: string;
  confidence: number;
}

interface ConsensusSummary {
  decision: string;
  confidence: number;
  summary: string | null;
}

interface SessionEntry {
  session_id: string;
  title: string;
  scenario: string;
  business_category: string;
  created_at: string | null;
  mode: "boardroom" | "workspace";
  has_report?: boolean;
  agents: AgentSummary[];
  consensus: ConsensusSummary | null;
}

const DECISION_COLORS: Record<string, string> = {
  approved: "#22c55e",
  conditional_approval: "#f59e0b",
  rejected: "#ef4444",
  executive_review_required: "#6366f1",
};

const POSITION_COLORS: Record<string, string> = {
  support: "#22c55e",
  conditional: "#f59e0b",
  neutral: "#6b7280",
  oppose: "#ef4444",
};

function SessionHistoryPage() {
  const [sessions, setSessions] = useState<SessionEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const resp = await fetch("http://localhost:8000/api/knowledge-hub/history");
      if (!resp.ok) throw new Error("Failed to fetch history");
      const data = await resp.json();
      setSessions(data.sessions || []);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load history");
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (iso: string | null) => {
    if (!iso) return "—";
    // Backend stores UTC — append Z to ensure proper timezone conversion
    const d = new Date(iso.endsWith("Z") ? iso : iso + "Z");
    return d.toLocaleString("en-IN", {
      month: "short", day: "numeric", year: "numeric",
      hour: "2-digit", minute: "2-digit", hour12: true,
      timeZone: "Asia/Kolkata",
    });
  };

  const formatDecision = (decision: string) =>
    decision.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());

  return (
    <div className="history-page">
      <div className="history-page__header">
        <h1 className="history-page__title">Session History</h1>
        <p className="history-page__subtitle">
          Past board meetings and workspace analyses stored in PostgreSQL
        </p>
        <button className="history-page__refresh" onClick={fetchHistory}>
          Refresh
        </button>
      </div>

      {loading && <div className="history-page__loading">Loading history...</div>}
      {error && <div className="history-page__error">{error}</div>}

      {!loading && sessions.length === 0 && (
        <div className="history-page__empty">
          <p>No sessions recorded yet.</p>
          <p>Run a board meeting or workspace analysis to see it here.</p>
        </div>
      )}

      <div className="history-page__list">
        {sessions.map((s) => (
          <div key={s.session_id} className="history-card">
            <div className="history-card__header">
              <span className={`history-card__mode history-card__mode--${s.mode}`}>
                {s.mode === "boardroom" ? "Board Meeting" : "Workspace"}
              </span>
              <span className="history-card__category">
                {(s.business_category || "").replace(/_/g, " ")}
              </span>
              <span className="history-card__date">{formatDate(s.created_at)}</span>
            </div>

            <p className="history-card__scenario">{s.scenario}</p>

            {s.agents.length > 0 && (
              <div className="history-card__agents">
                {s.agents.map((a) => (
                  <span
                    key={a.agent_id}
                    className="history-card__agent-badge"
                    style={{ borderColor: POSITION_COLORS[a.position] || "#6b7280" }}
                  >
                    <span className="history-card__agent-name">
                      {a.agent_id.replace("_", " ")}
                    </span>
                    <span
                      className="history-card__agent-pos"
                      style={{ color: POSITION_COLORS[a.position] || "#6b7280" }}
                    >
                      {a.position}
                    </span>
                  </span>
                ))}
              </div>
            )}

            {s.consensus && (
              <div
                className="history-card__consensus"
                style={{ borderColor: DECISION_COLORS[s.consensus.decision] || "#6366f1" }}
              >
                <span
                  className="history-card__decision"
                  style={{ color: DECISION_COLORS[s.consensus.decision] || "#6366f1" }}
                >
                  {formatDecision(s.consensus.decision)}
                </span>
                <span className="history-card__confidence">
                  {(s.consensus.confidence * 100).toFixed(0)}% confidence
                </span>
                {s.has_report && (
                  <a
                    href={`http://localhost:8000/api/knowledge-hub/report/${s.session_id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="history-card__report-link"
                  >
                    Download PDF
                  </a>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default SessionHistoryPage;
