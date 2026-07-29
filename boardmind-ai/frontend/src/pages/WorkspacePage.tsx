import { Link } from "react-router-dom";
import "./Pages.css";
import "./WorkspacePage.css";

const AGENTS = [
  {
    id: "finance",
    title: "Finance",
    role: "CFO",
    description: "Financial analysis, ROI, capital allocation, risk management",
    color: "var(--color-finance)",
    available: true,
  },
  {
    id: "marketing",
    title: "Marketing",
    role: "CMO",
    description: "Brand strategy, market positioning, customer acquisition",
    color: "var(--color-marketing)",
    available: true,
  },
  {
    id: "sales",
    title: "Sales",
    role: "CRO",
    description: "Revenue growth, pipeline health, customer relationships",
    color: "var(--color-sales)",
    available: true,
  },
  {
    id: "hr",
    title: "HR",
    role: "CHRO",
    description: "People strategy, talent management, organizational culture",
    color: "var(--color-hr)",
    available: true,
  },
  {
    id: "operations",
    title: "Operations",
    role: "COO",
    description: "Execution feasibility, process efficiency, delivery",
    color: "var(--color-operations)",
    available: true,
  },
  {
    id: "legal",
    title: "Legal",
    role: "GC",
    description: "Regulatory compliance, liability, corporate governance",
    color: "var(--color-legal)",
    available: true,
  },
  {
    id: "it",
    title: "IT",
    role: "CTO",
    description: "Technical feasibility, cybersecurity, infrastructure",
    color: "var(--color-it)",
    available: true,
  },
  {
    id: "business_analytics",
    title: "Analytics",
    role: "CDO",
    description: "Data-driven evidence, metrics, measurement frameworks",
    color: "var(--color-analytics)",
    available: true,
  },
];

function WorkspacePage() {
  return (
    <div className="page">
      <h1 className="page__title">Department Workspace</h1>
      <p className="page__subtitle">
        Select a department to get focused, single-perspective analysis of your
        business scenario.
      </p>

      <div className="workspace-grid">
        {AGENTS.map((agent) => {
          const content = (
            <div
              className={`workspace-card ${!agent.available ? "workspace-card--disabled" : ""}`}
              style={{ "--agent-color": agent.color } as React.CSSProperties}
            >
              <div className="workspace-card__header">
                <span className="workspace-card__badge">{agent.role}</span>
                {!agent.available && (
                  <span className="workspace-card__coming-soon">Coming Soon</span>
                )}
              </div>
              <h3 className="workspace-card__title">{agent.title}</h3>
              <p className="workspace-card__description">{agent.description}</p>
            </div>
          );

          return agent.available ? (
            <Link
              key={agent.id}
              to={`/workspace/${agent.id}`}
              className="workspace-card__link"
            >
              {content}
            </Link>
          ) : (
            <div key={agent.id} className="workspace-card__link">
              {content}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default WorkspacePage;
