import { AgentExecutionResult } from "../../services/boardroomApi";
import "./Boardroom.css";

interface DepartmentCardProps {
  result: AgentExecutionResult;
}

const AGENT_META: Record<string, { label: string; role: string; color: string }> = {
  finance: { label: "Finance", role: "CFO", color: "#22c55e" },
  marketing: { label: "Marketing", role: "CMO", color: "#a855f7" },
  sales: { label: "Sales", role: "CRO", color: "#3b82f6" },
  hr: { label: "HR", role: "CHRO", color: "#f97316" },
  operations: { label: "Operations", role: "COO", color: "#6b7280" },
  legal: { label: "Legal", role: "GC", color: "#ef4444" },
  it: { label: "IT", role: "CTO", color: "#14b8a6" },
  business_analytics: { label: "Analytics", role: "CDO", color: "#6366f1" },
};

function DepartmentCard({ result }: DepartmentCardProps) {
  const meta = AGENT_META[result.agent_id] || { label: result.agent_id, role: "?", color: "#6b7280" };
  const response = result.response;

  let position = "—";
  let confidence = 0;
  let summary = "";
  let topRisk = "";

  if (response) {
    const rawPos = String(response.position || "");
    position = rawPos.includes(".") ? rawPos.split(".").pop()!.toLowerCase() : rawPos.toLowerCase();
    confidence = Number(response.confidence || 0);
    summary = String(response.summary || "");
    const risks = response.risks as string[] | undefined;
    topRisk = risks && risks.length > 0 ? risks[0] : "";
  }

  const isFailed = result.status === "failed";

  return (
    <div
      className={`br-dept ${isFailed ? "br-dept--failed" : ""}`}
      style={{ "--dept-color": meta.color } as React.CSSProperties}
    >
      <div className="br-dept__header">
        <div className="br-dept__identity">
          <span className="br-dept__badge">{meta.role}</span>
          <span className="br-dept__name">{meta.label}</span>
        </div>
        <div className="br-dept__status">
          {isFailed ? (
            <span className="br-dept__status-badge br-dept__status-badge--failed">Failed</span>
          ) : (
            <span className={`br-dept__position br-dept__position--${position}`}>
              {position}
            </span>
          )}
        </div>
      </div>

      {!isFailed && response && (
        <div className="br-dept__body">
          <div className="br-dept__confidence">
            <div className="br-dept__confidence-bar">
              <div
                className="br-dept__confidence-fill"
                style={{ width: `${confidence * 100}%` }}
              />
            </div>
            <span className="br-dept__confidence-value">{(confidence * 100).toFixed(0)}%</span>
          </div>

          {summary && <p className="br-dept__summary">{summary}</p>}

          {topRisk && (
            <div className="br-dept__risk">
              <span className="br-dept__risk-label">Top Risk:</span> {topRisk}
            </div>
          )}

          <div className="br-dept__time">{result.execution_time_ms}ms</div>
        </div>
      )}

      {isFailed && (
        <div className="br-dept__body">
          <p className="br-dept__error">{result.error || "Execution failed"}</p>
        </div>
      )}
    </div>
  );
}

export default DepartmentCard;
