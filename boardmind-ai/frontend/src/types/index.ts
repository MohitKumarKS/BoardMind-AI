/**
 * Shared TypeScript types for BoardMind AI frontend.
 * These mirror the backend Pydantic models.
 */

export type Position = "support" | "oppose" | "neutral" | "conditional";

export type ConsensusLevel = "strong" | "moderate" | "split" | "none";

export type SessionStatus =
  | "created"
  | "round_1_active"
  | "round_1_complete"
  | "round_2_active"
  | "round_2_complete"
  | "round_3_active"
  | "round_3_complete"
  | "synthesizing"
  | "completed"
  | "error";

export interface AgentIdentity {
  agent_id: string;
  title: string;
  short: string;
  domain: string;
  color: string;
}

export interface AgentResponse {
  agent_id: string;
  round: number;
  position: Position;
  confidence: number;
  domain_assessment: Record<string, string>;
  summary: string;
  rationale: string;
  risks: string[];
  conditions: string[];
  references_to: string[];
}

export interface Session {
  session_id: string;
  scenario: string;
  mode: "workspace" | "boardroom";
  status: SessionStatus;
  participating_agents: string[];
  current_round: number;
}

export interface ConsensusResult {
  consensus_score: number;
  consensus_level: ConsensusLevel;
  executive_summary: string;
  key_agreements: string[];
  key_disagreements: string[];
  dissenting_views: Record<string, unknown>[];
  risk_matrix: Record<string, unknown>[];
  recommended_next_steps: string[];
}

export interface Report {
  report_id: string;
  session_id: string;
  content: string;
  format: "markdown" | "pdf" | "html";
}
