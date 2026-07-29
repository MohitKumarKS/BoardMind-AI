import { AgentExecutionResult } from "../../services/boardroomApi";
import "./Boardroom.css";

interface ExecutionTimelineProps {
  results: AgentExecutionResult[];
  totalTimeMs: number;
}

const AGENT_LABELS: Record<string, string> = {
  finance: "Finance (CFO)",
  marketing: "Marketing (CMO)",
  sales: "Sales (CRO)",
  hr: "HR (CHRO)",
  operations: "Operations (COO)",
  legal: "Legal (GC)",
  it: "IT (CTO)",
  business_analytics: "Analytics (CDO)",
};

function ExecutionTimeline({ results, totalTimeMs }: ExecutionTimelineProps) {
  return (
    <div className="br-timeline">
      <div className="br-timeline__header">
        <h4 className="br-timeline__title">Execution Timeline</h4>
        <span className="br-timeline__total">Total: {totalTimeMs}ms (parallel)</span>
      </div>
      <div className="br-timeline__list">
        {results.map((r) => (
          <div key={r.agent_id} className={`br-timeline__item br-timeline__item--${r.status}`}>
            <span className="br-timeline__agent">
              {AGENT_LABELS[r.agent_id] || r.agent_id}
            </span>
            <span className="br-timeline__status">{r.status}</span>
            <span className="br-timeline__time">{r.execution_time_ms}ms</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ExecutionTimeline;
