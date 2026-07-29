import { ConsensusResult } from "../../services/boardroomApi";
import "./Boardroom.css";

interface ExecutiveSummaryProps {
  consensus: ConsensusResult;
}

function ExecutiveSummary({ consensus }: ExecutiveSummaryProps) {
  return (
    <div className="br-summary">
      {consensus.key_risks.length > 0 && (
        <div className="br-summary__section">
          <h4 className="br-summary__section-title">Key Risks</h4>
          <ul className="br-summary__list br-summary__list--risks">
            {consensus.key_risks.slice(0, 10).map((risk, idx) => (
              <li key={idx}>{risk}</li>
            ))}
          </ul>
        </div>
      )}

      {consensus.recommended_actions.length > 0 && (
        <div className="br-summary__section">
          <h4 className="br-summary__section-title">Recommended Actions</h4>
          <ul className="br-summary__list br-summary__list--actions">
            {consensus.recommended_actions.slice(0, 10).map((action, idx) => (
              <li key={idx}>{action}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="br-summary__section">
        <h4 className="br-summary__section-title">Participating Departments</h4>
        <div className="br-summary__agents">
          {consensus.participating_agents.map((agent) => (
            <span key={agent} className="br-summary__agent-tag">
              {agent.replace("_", " ")}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ExecutiveSummary;
