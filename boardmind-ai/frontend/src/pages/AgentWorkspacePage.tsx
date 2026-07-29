import { useState } from "react";
import { analyzeAgent } from "../services/api";
import "./AgentWorkspacePage.css";

export interface AgentConfig {
  id: string;
  title: string;
  role: string;
  subtitle: string;
  color: string;
  endpoint: string;
  examples: { label: string; scenario: string }[];
  domainFields: { key: string; label: string }[];
  extraListFields?: { key: string; label: string; bulletColor: string }[];
  extraTextField?: { key: string; label: string };
}

interface AgentResponse {
  agent_id: string;
  round: number;
  position: "support" | "oppose" | "neutral" | "conditional";
  confidence: number;
  domain_assessment: Record<string, unknown>;
  summary: string;
  rationale: string;
  risks: string[];
  conditions: string[];
  metrics_to_track: string[];
  references_to: string[];
  [key: string]: unknown;
}

interface AgentWorkspacePageProps {
  config: AgentConfig;
}

function AgentWorkspacePage({ config }: AgentWorkspacePageProps) {
  const [scenario, setScenario] = useState("");
  const [context, setContext] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [response, setResponse] = useState<AgentResponse | null>(null);

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
      const result = await analyzeAgent(config.endpoint, {
        scenario: scenario.trim(),
        context: context.trim() || null,
      });
      setResponse(result as AgentResponse);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  const loadExample = (idx: number) => {
    setScenario(config.examples[idx].scenario);
    setContext("");
    setResponse(null);
    setError(null);
  };

  const style = { "--agent-color": config.color } as React.CSSProperties;

  return (
    <div className="agent-page" style={style}>
      <div className="agent-page__header">
        <div className="agent-page__badge">{config.role}</div>
        <div>
          <h1 className="agent-page__title">{config.title}</h1>
          <p className="agent-page__subtitle">{config.subtitle}</p>
        </div>
      </div>

      <form className="agent-form" onSubmit={handleSubmit}>
        <div className="agent-form__field">
          <label className="agent-form__label" htmlFor={`${config.id}-scenario`}>
            Business Proposal
          </label>
          <textarea
            id={`${config.id}-scenario`}
            className="agent-form__textarea"
            value={scenario}
            onChange={(e) => setScenario(e.target.value)}
            placeholder={`Describe the business proposal you want the ${config.role} to analyze...`}
            rows={6}
            required
            minLength={20}
          />
        </div>

        <div className="agent-form__field">
          <label className="agent-form__label" htmlFor={`${config.id}-context`}>
            Additional Context{" "}
            <span className="agent-form__optional">(optional)</span>
          </label>
          <textarea
            id={`${config.id}-context`}
            className="agent-form__textarea agent-form__textarea--small"
            value={context}
            onChange={(e) => setContext(e.target.value)}
            placeholder="Additional data, constraints, or context..."
            rows={3}
          />
        </div>

        <div className="agent-form__actions">
          <button
            type="submit"
            className="agent-form__submit"
            disabled={loading || scenario.trim().length < 20}
          >
            {loading ? "Analyzing..." : `Analyze as ${config.role}`}
          </button>
        </div>

        {config.examples.length > 0 && (
          <div className="agent-form__examples">
            <span className="agent-form__examples-label">Try an example:</span>
            <div className="agent-form__examples-list">
              {config.examples.map((ex, idx) => (
                <button
                  key={idx}
                  type="button"
                  className="agent-form__example-btn"
                  onClick={() => loadExample(idx)}
                >
                  {ex.label}
                </button>
              ))}
            </div>
          </div>
        )}
      </form>

      {error && (
        <div className="agent-error">
          <p>{error}</p>
        </div>
      )}

      {loading && (
        <div className="agent-loading">
          <div className="agent-loading__spinner" />
          <p>The {config.role} is analyzing your proposal...</p>
        </div>
      )}

      {response && (
        <AgentResponseDisplay response={response} config={config} />
      )}
    </div>
  );
}

interface AgentResponseDisplayProps {
  response: AgentResponse;
  config: AgentConfig;
}

function AgentResponseDisplay({ response, config }: AgentResponseDisplayProps) {
  const domainAssessment = response.domain_assessment;

  return (
    <div className="agent-response">
      {/* Position & Confidence Header */}
      <div className="agent-response__header">
        <div className={`agent-position agent-position--${response.position}`}>
          <span className="agent-position__label">Position</span>
          <span className="agent-position__value">{response.position}</span>
        </div>
        <div className="agent-confidence">
          <span className="agent-confidence__label">Confidence</span>
          <div className="agent-confidence__bar">
            <div
              className="agent-confidence__fill"
              style={{ width: `${response.confidence * 100}%` }}
            />
          </div>
          <span className="agent-confidence__value">
            {(response.confidence * 100).toFixed(0)}%
          </span>
        </div>
      </div>

      {/* Summary */}
      <div className="agent-card">
        <h3 className="agent-card__title">Summary</h3>
        <p className="agent-card__text">{response.summary}</p>
      </div>

      {/* Domain-specific Metrics */}
      {config.domainFields.length > 0 && (
        <div className="agent-card">
          <h3 className="agent-card__title">Domain Assessment</h3>
          <div className="agent-metrics">
            {config.domainFields.map((field) => {
              const value = domainAssessment[field.key];
              const isRiskLevel =
                field.key === "risk_level" &&
                typeof value === "string" &&
                ["low", "medium", "high"].includes(value);

              return (
                <div className="agent-metric" key={field.key}>
                  <span className="agent-metric__label">{field.label}</span>
                  {isRiskLevel ? (
                    <span
                      className={`agent-risk-badge agent-risk-badge--${value}`}
                    >
                      {value as string}
                    </span>
                  ) : (
                    <p className="agent-metric__value">
                      {value != null ? String(value) : "—"}
                    </p>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Rationale */}
      <div className="agent-card">
        <h3 className="agent-card__title">Detailed Rationale</h3>
        <div className="agent-card__rationale">
          {response.rationale.split("\n\n").map((para, idx) => (
            <p key={idx}>{para}</p>
          ))}
        </div>
      </div>

      {/* Risks */}
      {response.risks.length > 0 && (
        <div className="agent-card">
          <h3 className="agent-card__title">Risks</h3>
          <ul className="agent-list agent-list--risks">
            {response.risks.map((risk, idx) => (
              <li key={idx}>{risk}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Conditions */}
      {response.conditions.length > 0 && (
        <div className="agent-card">
          <h3 className="agent-card__title">Conditions for Support</h3>
          <ul className="agent-list agent-list--conditions">
            {response.conditions.map((condition, idx) => (
              <li key={idx}>{condition}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Metrics to Track */}
      {response.metrics_to_track && response.metrics_to_track.length > 0 && (
        <div className="agent-card">
          <h3 className="agent-card__title">Recommended KPIs</h3>
          <ul className="agent-list agent-list--accent">
            {response.metrics_to_track.map((metric, idx) => (
              <li key={idx}>{metric}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Extra list fields (agent-specific) */}
      {(config.extraListFields ?? []).map((field) => {
        const raw = response[field.key];
        if (!Array.isArray(raw) || raw.length === 0) return null;
        const items = raw as string[];
        return (
          <div className="agent-card" key={field.key}>
            <h3 className="agent-card__title">{field.label}</h3>
            <ul
              className="agent-list agent-list--custom"
              style={{ "--bullet-color": field.bulletColor } as React.CSSProperties}
            >
              {items.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          </div>
        );
      })}

      {/* Extra text field (agent-specific) */}
      {config.extraTextField != null && response[config.extraTextField.key] != null && (
        <div className="agent-card">
          <h3 className="agent-card__title">{config.extraTextField.label}</h3>
          <p className="agent-card__extra-text">
            {String(response[config.extraTextField.key])}
          </p>
        </div>
      )}
    </div>
  );
}

export default AgentWorkspacePage;
