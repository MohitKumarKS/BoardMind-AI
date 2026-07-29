import { useState } from "react";
import { analyzeFinance, FinanceResponse } from "../services/api";
import "./FinanceWorkspacePage.css";

const EXAMPLE_SCENARIOS = [
  {
    label: "New Product Launch",
    scenario:
      "We are considering launching a new B2B SaaS product targeting mid-market companies (500-2000 employees). The product is an AI-powered analytics dashboard. Estimated development cost is $400K over 6 months, with a target price of $2,000/month per customer. Our sales team believes we can acquire 50 customers in Year 1.",
  },
  {
    label: "Market Expansion",
    scenario:
      "Our US-based e-commerce platform is considering expanding into the European market (UK and Germany). This requires local warehousing, multilingual support, and GDPR compliance. The European market represents 30% of our TAM. A competitor entered Europe last year and captured 8% share in 6 months.",
  },
  {
    label: "Engineering Hiring",
    scenario:
      "The engineering team requests 8 additional software engineers to accelerate development. Current team is 12. VP Engineering claims this reduces roadmap from 18 to 10 months, enabling earlier launch of three features projected to generate $3.5M additional ARR.",
  },
  {
    label: "AI Infrastructure",
    scenario:
      "The CTO proposes investing in dedicated AI/ML infrastructure (GPU cluster, MLOps platform, 3-person ML team) to replace third-party AI APIs costing $45K/month and growing 25% MoM. Proposed: $1.2M upfront + $30K/month ops. ML team: $600K/year.",
  },
  {
    label: "New Office",
    scenario:
      "Leadership proposes opening a second office in Austin, TX. Plan includes 15,000 sq ft lease, relocation packages for 5 senior leaders, and hiring 30 local employees over 18 months. Austin salary is 20% below SF for equivalent roles.",
  },
];

function FinanceWorkspacePage() {
  const [scenario, setScenario] = useState("");
  const [context, setContext] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [response, setResponse] = useState<FinanceResponse | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (scenario.trim().length < 20) {
      setError("Please provide a more detailed scenario (at least 20 characters).");
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const result = await analyzeFinance({
        scenario: scenario.trim(),
        context: context.trim() || null,
      });
      setResponse(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  const loadExample = (idx: number) => {
    setScenario(EXAMPLE_SCENARIOS[idx].scenario);
    setContext("");
    setResponse(null);
    setError(null);
  };

  return (
    <div className="finance-page">
      <div className="finance-page__header">
        <div className="finance-page__badge">CFO</div>
        <div>
          <h1 className="finance-page__title">Finance Agent</h1>
          <p className="finance-page__subtitle">
            Chief Financial Officer perspective — quantitative analysis,
            risk-adjusted returns, and capital efficiency
          </p>
        </div>
      </div>

      <form className="finance-form" onSubmit={handleSubmit}>
        <div className="finance-form__field">
          <label className="finance-form__label" htmlFor="scenario">
            Business Proposal
          </label>
          <textarea
            id="scenario"
            className="finance-form__textarea"
            value={scenario}
            onChange={(e) => setScenario(e.target.value)}
            placeholder="Describe the business proposal you want the CFO to analyze..."
            rows={6}
            required
            minLength={20}
          />
        </div>

        <div className="finance-form__field">
          <label className="finance-form__label" htmlFor="context">
            Additional Context{" "}
            <span className="finance-form__optional">(optional)</span>
          </label>
          <textarea
            id="context"
            className="finance-form__textarea finance-form__textarea--small"
            value={context}
            onChange={(e) => setContext(e.target.value)}
            placeholder="Financial data, constraints, runway, revenue figures..."
            rows={3}
          />
        </div>

        <div className="finance-form__actions">
          <button
            type="submit"
            className="finance-form__submit"
            disabled={loading || scenario.trim().length < 20}
          >
            {loading ? "Analyzing..." : "Analyze as CFO"}
          </button>
        </div>

        <div className="finance-form__examples">
          <span className="finance-form__examples-label">Try an example:</span>
          <div className="finance-form__examples-list">
            {EXAMPLE_SCENARIOS.map((ex, idx) => (
              <button
                key={idx}
                type="button"
                className="finance-form__example-btn"
                onClick={() => loadExample(idx)}
              >
                {ex.label}
              </button>
            ))}
          </div>
        </div>
      </form>

      {error && (
        <div className="finance-error">
          <p>{error}</p>
        </div>
      )}

      {loading && (
        <div className="finance-loading">
          <div className="finance-loading__spinner" />
          <p>The CFO is analyzing your proposal...</p>
        </div>
      )}

      {response && <FinanceResponseDisplay response={response} />}
    </div>
  );
}

function FinanceResponseDisplay({ response }: { response: FinanceResponse }) {
  return (
    <div className="finance-response">
      {/* Position & Confidence Header */}
      <div className="finance-response__header">
        <div className={`finance-position finance-position--${response.position}`}>
          <span className="finance-position__label">Position</span>
          <span className="finance-position__value">{response.position}</span>
        </div>
        <div className="finance-confidence">
          <span className="finance-confidence__label">Confidence</span>
          <div className="finance-confidence__bar">
            <div
              className="finance-confidence__fill"
              style={{ width: `${response.confidence * 100}%` }}
            />
          </div>
          <span className="finance-confidence__value">
            {(response.confidence * 100).toFixed(0)}%
          </span>
        </div>
      </div>

      {/* Summary */}
      <div className="finance-card">
        <h3 className="finance-card__title">Summary</h3>
        <p className="finance-card__text">{response.summary}</p>
      </div>

      {/* Financial Metrics */}
      <div className="finance-card">
        <h3 className="finance-card__title">Financial Impact Assessment</h3>
        <div className="finance-metrics">
          <div className="finance-metric">
            <span className="finance-metric__label">Revenue Impact</span>
            <p className="finance-metric__value">
              {response.domain_assessment.revenue_impact}
            </p>
          </div>
          <div className="finance-metric">
            <span className="finance-metric__label">Cost Impact</span>
            <p className="finance-metric__value">
              {response.domain_assessment.cost_impact}
            </p>
          </div>
          <div className="finance-metric">
            <span className="finance-metric__label">ROI Estimate</span>
            <p className="finance-metric__value">
              {response.domain_assessment.roi_estimate}
            </p>
          </div>
          <div className="finance-metric">
            <span className="finance-metric__label">Payback Period</span>
            <p className="finance-metric__value">
              {response.domain_assessment.payback_period}
            </p>
          </div>
          <div className="finance-metric">
            <span className="finance-metric__label">Risk Level</span>
            <span
              className={`finance-risk-badge finance-risk-badge--${response.domain_assessment.risk_level}`}
            >
              {response.domain_assessment.risk_level}
            </span>
          </div>
        </div>
      </div>

      {/* Rationale */}
      <div className="finance-card">
        <h3 className="finance-card__title">Detailed Rationale</h3>
        <div className="finance-card__rationale">
          {response.rationale.split("\n\n").map((para, idx) => (
            <p key={idx}>{para}</p>
          ))}
        </div>
      </div>

      {/* Risks */}
      <div className="finance-card">
        <h3 className="finance-card__title">Financial Risks</h3>
        <ul className="finance-list finance-list--risks">
          {response.risks.map((risk, idx) => (
            <li key={idx}>{risk}</li>
          ))}
        </ul>
      </div>

      {/* Conditions */}
      {response.conditions.length > 0 && (
        <div className="finance-card">
          <h3 className="finance-card__title">Conditions for Support</h3>
          <ul className="finance-list finance-list--conditions">
            {response.conditions.map((condition, idx) => (
              <li key={idx}>{condition}</li>
            ))}
          </ul>
        </div>
      )}

      {/* KPIs */}
      <div className="finance-card">
        <h3 className="finance-card__title">Recommended KPIs</h3>
        <ul className="finance-list finance-list--kpis">
          {response.metrics_to_track.map((metric, idx) => (
            <li key={idx}>{metric}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default FinanceWorkspacePage;
