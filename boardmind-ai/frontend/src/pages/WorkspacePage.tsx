import { Link } from "react-router-dom";
import "./Pages.css";
import "./WorkspacePage.css";

const AGENTS = [
  {
    id: "ceo",
    title: "CEO",
    role: "CEO",
    description: "Strategic vision, corporate direction, stakeholder alignment",
    color: "var(--color-ceo)",
    available: true,
  },
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
  {
    id: "ciso",
    title: "Security",
    role: "CISO",
    description: "Cybersecurity, threat assessment, data protection, compliance",
    color: "var(--color-ciso)",
    available: true,
  },
  {
    id: "risk",
    title: "Risk",
    role: "CRO-Risk",
    description: "Enterprise risk management, quantification, scenario analysis",
    color: "var(--color-risk)",
    available: true,
  },
  {
    id: "compliance",
    title: "Compliance",
    role: "CCO",
    description: "Regulatory compliance, governance frameworks, audit readiness",
    color: "var(--color-compliance)",
    available: true,
  },
  {
    id: "strategy",
    title: "Strategy",
    role: "CSO",
    description: "Competitive analysis, market positioning, strategic planning",
    color: "var(--color-strategy)",
    available: true,
  },
  {
    id: "product",
    title: "Product",
    role: "CPO",
    description: "Product strategy, roadmap, product-market fit, UX",
    color: "var(--color-product)",
    available: true,
  },
  {
    id: "customer_success",
    title: "Customer Success",
    role: "CCusO",
    description: "Customer retention, NPS/CSAT, lifecycle management",
    color: "var(--color-customer-success)",
    available: true,
  },
  {
    id: "supply_chain",
    title: "Supply Chain",
    role: "CSCO",
    description: "Procurement, logistics, vendor management, fulfillment",
    color: "var(--color-supply-chain)",
    available: true,
  },
  {
    id: "esg",
    title: "ESG",
    role: "ESG",
    description: "Sustainability, carbon impact, social responsibility",
    color: "var(--color-esg)",
    available: true,
  },
  {
    id: "ai_governance",
    title: "AI Governance",
    role: "AIGO",
    description: "AI ethics, algorithmic fairness, responsible AI deployment",
    color: "var(--color-ai-governance)",
    available: true,
  },
  {
    id: "innovation",
    title: "Innovation",
    role: "CIO-Inn",
    description: "R&D strategy, emerging tech, innovation pipeline, patents",
    color: "var(--color-innovation)",
    available: true,
  },
  {
    id: "investor_relations",
    title: "Investor Relations",
    role: "IRO",
    description: "Shareholder communication, market perception, earnings",
    color: "var(--color-investor-relations)",
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
