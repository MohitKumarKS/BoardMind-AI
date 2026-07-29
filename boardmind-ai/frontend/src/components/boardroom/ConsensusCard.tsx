import { ConsensusResult } from "../../services/boardroomApi";
import "./Boardroom.css";

interface ConsensusCardProps {
  consensus: ConsensusResult;
}

const DECISION_CONFIG: Record<string, { label: string; color: string; bg: string }> = {
  approved: { label: "Approved", color: "#22c55e", bg: "rgba(34,197,94,0.1)" },
  conditional_approval: { label: "Conditional Approval", color: "#f59e0b", bg: "rgba(245,158,11,0.1)" },
  rejected: { label: "Rejected", color: "#ef4444", bg: "rgba(239,68,68,0.1)" },
  executive_review_required: { label: "Executive Review Required", color: "#6366f1", bg: "rgba(99,102,241,0.1)" },
};

function ConsensusCard({ consensus }: ConsensusCardProps) {
  const config = DECISION_CONFIG[consensus.decision] || DECISION_CONFIG.executive_review_required;

  return (
    <div className="br-consensus">
      <div className="br-consensus__header">
        <h3 className="br-consensus__title">Board Decision</h3>
      </div>

      <div
        className="br-consensus__decision"
        style={{ backgroundColor: config.bg, borderColor: config.color }}
      >
        <span className="br-consensus__decision-label" style={{ color: config.color }}>
          {config.label}
        </span>
        <span className="br-consensus__confidence">
          Confidence: {(consensus.confidence * 100).toFixed(0)}%
        </span>
      </div>

      <div className="br-consensus__votes">
        <div className="br-consensus__vote br-consensus__vote--support">
          <span className="br-consensus__vote-count">{consensus.support_count}</span>
          <span className="br-consensus__vote-label">Support</span>
        </div>
        <div className="br-consensus__vote br-consensus__vote--conditional">
          <span className="br-consensus__vote-count">{consensus.conditional_count}</span>
          <span className="br-consensus__vote-label">Conditional</span>
        </div>
        <div className="br-consensus__vote br-consensus__vote--neutral">
          <span className="br-consensus__vote-count">{consensus.neutral_count}</span>
          <span className="br-consensus__vote-label">Neutral</span>
        </div>
        <div className="br-consensus__vote br-consensus__vote--oppose">
          <span className="br-consensus__vote-count">{consensus.oppose_count}</span>
          <span className="br-consensus__vote-label">Oppose</span>
        </div>
      </div>

      {consensus.conflict_detected && (
        <div className="br-consensus__conflict">
          <span className="br-consensus__conflict-badge">Conflict Detected</span>
          <div className="br-consensus__conflict-list">
            {consensus.conflicting_agents.map((c, idx) => (
              <span key={idx} className="br-consensus__conflict-pair">
                {c.agent_supporting.replace("_", " ")} vs {c.agent_opposing.replace("_", " ")}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="br-consensus__summary">
        <p>{consensus.executive_summary}</p>
      </div>
    </div>
  );
}

export default ConsensusCard;
