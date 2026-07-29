/**
 * Boardroom API service for Executive Boardroom operations.
 */

const API_BASE = "http://localhost:8000/api";

export interface OrchestrateRequest {
  scenario: string;
  optional_context?: string | null;
}

export interface AgentExecutionResult {
  agent_id: string;
  response: Record<string, unknown> | null;
  execution_time_ms: number;
  status: "completed" | "failed" | "timeout";
  error: string | null;
}

export interface ExecutionSummary {
  total_agents_selected: number;
  total_agents_completed: number;
  total_agents_failed: number;
  total_execution_time_ms: number;
}

export interface OrchestrateResponse {
  session_id: string;
  scenario: string;
  business_category: string;
  selected_agents: string[];
  execution_summary: ExecutionSummary;
  responses: AgentExecutionResult[];
}

export interface ConsensusResult {
  decision: "approved" | "conditional_approval" | "rejected" | "executive_review_required";
  confidence: number;
  support_count: number;
  conditional_count: number;
  neutral_count: number;
  oppose_count: number;
  participating_agents: string[];
  conflict_detected: boolean;
  conflicting_agents: { agent_supporting: string; agent_opposing: string }[];
  executive_summary: string;
  key_risks: string[];
  recommended_actions: string[];
}

export async function orchestrate(request: OrchestrateRequest): Promise<OrchestrateResponse> {
  const response = await fetch(`${API_BASE}/boardroom/orchestrate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || `Orchestration failed: ${response.status}`);
  }

  return response.json();
}

export async function runConsensus(sessionId: string): Promise<ConsensusResult> {
  const response = await fetch(`${API_BASE}/boardroom/consensus`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || `Consensus failed: ${response.status}`);
  }

  return response.json();
}


export interface MCPFileResult {
  source: string;
  filename: string;
  file_size_bytes: number;
  text?: string;
  data?: Record<string, unknown>[];
  columns?: string[];
  total_rows?: number;
  error?: string;
  [key: string]: unknown;
}

export async function uploadFile(file: File): Promise<MCPFileResult> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/mcp/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Upload failed" }));
    throw new Error(error.detail || `Upload failed: ${response.status}`);
  }

  return response.json();
}
