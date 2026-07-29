/**
 * API service for BoardMind AI backend communication.
 */

const API_BASE = "http://localhost:8000/api";

export interface FinanceRequest {
  scenario: string;
  context?: string | null;
}

export interface FinanceDomainAssessment {
  revenue_impact: string;
  cost_impact: string;
  roi_estimate: string;
  payback_period: string;
  risk_level: "low" | "medium" | "high";
}

export interface FinanceResponse {
  agent_id: string;
  round: number;
  position: "support" | "oppose" | "neutral" | "conditional";
  confidence: number;
  domain_assessment: FinanceDomainAssessment;
  summary: string;
  rationale: string;
  risks: string[];
  conditions: string[];
  metrics_to_track: string[];
  references_to: string[];
}

export async function analyzeFinance(
  request: FinanceRequest
): Promise<FinanceResponse> {
  const response = await fetch(`${API_BASE}/workspace/finance`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || `Request failed: ${response.status}`);
  }

  return response.json();
}

export async function analyzeAgent(
  endpoint: string,
  request: { scenario: string; context?: string | null }
): Promise<Record<string, unknown>> {
  const response = await fetch(`${API_BASE}/workspace/${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || `Request failed: ${response.status}`);
  }

  return response.json();
}
