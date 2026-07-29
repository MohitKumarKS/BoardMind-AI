import { useRef } from "react";
import "./Boardroom.css";

interface ScenarioInputProps {
  scenario: string;
  context: string;
  loading: boolean;
  attachedFile: File | null;
  onScenarioChange: (value: string) => void;
  onContextChange: (value: string) => void;
  onFileAttach: (file: File | null) => void;
  onSubmit: () => void;
}

const EXAMPLES = [
  { label: "Product Launch", text: "We are considering launching a new AI-powered analytics SaaS product targeting mid-market companies at $2,000/month with a 6-month development timeline and $500K budget." },
  { label: "Market Expansion", text: "Our US-based platform is considering expanding into European markets starting with UK and Germany, requiring local operations, GDPR compliance, and localized marketing." },
  { label: "Cost Reduction", text: "We need to reduce operational costs by 30% this year including potential headcount adjustments, office consolidation, and vendor renegotiation." },
  { label: "AI Investment", text: "The CTO proposes investing $1.2M in dedicated AI infrastructure to replace third-party APIs costing $45K/month and growing 25% month-over-month." },
];

const ACCEPTED_TYPES = ".csv,.xlsx,.xls,.txt,.md,.pdf,.docx";

function ScenarioInput({ scenario, context, loading, attachedFile, onScenarioChange, onContextChange, onFileAttach, onSubmit }: ScenarioInputProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    onFileAttach(file);
  };

  const handleRemoveFile = () => {
    onFileAttach(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="br-input">
      <div className="br-input__header">
        <h2 className="br-input__title">Business Scenario</h2>
        <p className="br-input__subtitle">
          Present your business decision to the executive board
        </p>
      </div>

      <div className="br-input__field">
        <textarea
          className="br-input__textarea"
          value={scenario}
          onChange={(e) => onScenarioChange(e.target.value)}
          placeholder="Describe the business proposal, decision, or scenario you want the executive board to analyze..."
          rows={5}
          disabled={loading}
        />
      </div>

      <div className="br-input__field">
        <label className="br-input__label">
          Additional Context <span className="br-input__optional">(optional)</span>
        </label>
        <textarea
          className="br-input__textarea br-input__textarea--small"
          value={context}
          onChange={(e) => onContextChange(e.target.value)}
          placeholder="Financial data, constraints, timeline requirements..."
          rows={2}
          disabled={loading}
        />
      </div>

      <div className="br-input__field">
        <label className="br-input__label">
          Attach File <span className="br-input__optional">(optional — CSV, Excel, PDF, DOCX, TXT)</span>
        </label>
        <div className="br-input__file-row">
          <input
            ref={fileInputRef}
            type="file"
            accept={ACCEPTED_TYPES}
            onChange={handleFileChange}
            disabled={loading}
            className="br-input__file-input"
          />
          {attachedFile && (
            <div className="br-input__file-badge">
              <span className="br-input__file-name">{attachedFile.name}</span>
              <span className="br-input__file-size">
                ({(attachedFile.size / 1024).toFixed(1)} KB)
              </span>
              <button
                type="button"
                className="br-input__file-remove"
                onClick={handleRemoveFile}
                disabled={loading}
              >
                Remove
              </button>
            </div>
          )}
        </div>
      </div>

      <div className="br-input__actions">
        <button
          className="br-input__submit"
          onClick={onSubmit}
          disabled={loading || scenario.trim().length < 20}
        >
          {loading ? "Meeting in Progress..." : "Start Board Meeting"}
        </button>
      </div>

      <div className="br-input__examples">
        <span className="br-input__examples-label">Quick scenarios:</span>
        <div className="br-input__examples-list">
          {EXAMPLES.map((ex, idx) => (
            <button
              key={idx}
              className="br-input__example-btn"
              onClick={() => { onScenarioChange(ex.text); onContextChange(""); }}
              disabled={loading}
            >
              {ex.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ScenarioInput;
