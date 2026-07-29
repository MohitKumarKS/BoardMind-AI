import "./Boardroom.css";

export type MeetingStage =
  | "idle"
  | "routing"
  | "executing"
  | "consensus"
  | "complete"
  | "error";

interface MeetingProgressProps {
  stage: MeetingStage;
  category?: string;
  agentCount?: number;
}

const STAGES = [
  { key: "routing", label: "Decision Router", description: "Classifying scenario" },
  { key: "executing", label: "Department Execution", description: "Agents analyzing" },
  { key: "consensus", label: "Consensus Engine", description: "Building recommendation" },
  { key: "complete", label: "Complete", description: "Meeting concluded" },
];

function MeetingProgress({ stage, category, agentCount }: MeetingProgressProps) {
  if (stage === "idle") return null;

  const activeIndex = STAGES.findIndex((s) => s.key === stage);

  return (
    <div className="br-progress">
      <div className="br-progress__header">
        <h3 className="br-progress__title">Meeting Progress</h3>
        {category && (
          <span className="br-progress__category">{category.replace(/_/g, " ")}</span>
        )}
        {agentCount !== undefined && agentCount > 0 && (
          <span className="br-progress__agents">{agentCount} departments</span>
        )}
      </div>
      <div className="br-progress__steps">
        {STAGES.map((s, idx) => {
          let status: "done" | "active" | "pending" = "pending";
          if (idx < activeIndex || stage === "complete") status = "done";
          else if (idx === activeIndex) status = "active";

          return (
            <div key={s.key} className={`br-progress__step br-progress__step--${status}`}>
              <div className="br-progress__dot" />
              <div className="br-progress__step-info">
                <span className="br-progress__step-label">{s.label}</span>
                {status === "active" && (
                  <span className="br-progress__step-desc">{s.description}</span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default MeetingProgress;
