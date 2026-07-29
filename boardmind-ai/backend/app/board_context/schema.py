"""Board Context schemas.

Defines the shared state of a single executive board meeting.
Exists only for the duration of one orchestration session.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class AgentResult(BaseModel):
    """Result from a single department agent within a board session."""

    agent_id: str = Field(..., description="Department agent identifier")
    status: str = Field(
        default="pending",
        description="Agent status: pending | running | completed | failed",
    )
    started_at: Optional[datetime] = Field(
        default=None, description="When agent execution began"
    )
    completed_at: Optional[datetime] = Field(
        default=None, description="When agent execution finished"
    )
    execution_time_ms: Optional[int] = Field(
        default=None, description="Execution duration in milliseconds"
    )
    response: Optional[dict[str, Any]] = Field(
        default=None, description="The agent's full structured response"
    )
    error: Optional[str] = Field(
        default=None, description="Error message if agent failed"
    )


class ExecutionMetadata(BaseModel):
    """Execution summary for the board session."""

    total_agents: int = Field(default=0, description="Total agents selected")
    completed_agents: int = Field(default=0, description="Agents completed successfully")
    failed_agents: int = Field(default=0, description="Agents that failed")
    total_execution_time_ms: int = Field(
        default=0, description="Total wall-clock time (parallel)"
    )


class ConsensusResult(BaseModel):
    """Result produced by the Consensus Engine."""

    decision: str = Field(
        ...,
        description="Final decision: approved | conditional_approval | rejected | executive_review_required",
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Overall confidence in the decision"
    )
    support_count: int = Field(default=0, description="Agents that support")
    conditional_count: int = Field(default=0, description="Agents with conditional support")
    neutral_count: int = Field(default=0, description="Agents that are neutral")
    oppose_count: int = Field(default=0, description="Agents that oppose")
    participating_agents: list[str] = Field(
        default_factory=list, description="Agents that contributed to consensus"
    )
    conflict_detected: bool = Field(
        default=False, description="Whether conflicting positions were found"
    )
    conflicting_agents: list[dict[str, str]] = Field(
        default_factory=list,
        description="Pairs of agents with conflicting positions",
    )
    executive_summary: str = Field(
        ..., description="Concise summary of the consensus outcome"
    )
    key_risks: list[str] = Field(
        default_factory=list, description="Aggregated risks from all agents"
    )
    recommended_actions: list[str] = Field(
        default_factory=list, description="Aggregated recommendations"
    )


class BoardContext(BaseModel):
    """Shared state of one executive board meeting.

    This is the complete representation of a single deliberation session.
    It accumulates data as the orchestration progresses:
    - Created when a session starts
    - Updated as each agent completes
    - Analyzed by the Consensus Engine
    - Read by future modules (Report Generator)
    """

    session_id: str = Field(..., description="Unique session identifier")
    scenario: str = Field(..., description="The business scenario under discussion")
    optional_context: Optional[str] = Field(
        default=None, description="Additional context provided by user"
    )
    business_category: str = Field(
        ..., description="Category assigned by Decision Router"
    )
    selected_agents: list[str] = Field(
        ..., description="Agents selected to participate"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Session creation time"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Last update time"
    )
    status: str = Field(
        default="created",
        description="Session status: created | in_progress | completed | failed",
    )
    agent_results: dict[str, AgentResult] = Field(
        default_factory=dict,
        description="Results keyed by agent_id",
    )
    shared_notes: list[str] = Field(
        default_factory=list,
        description="Shared meeting notes (for future modules)",
    )
    execution_metadata: ExecutionMetadata = Field(
        default_factory=ExecutionMetadata,
        description="Execution summary statistics",
    )
    consensus_result: Optional[ConsensusResult] = Field(
        default=None,
        description="Consensus Engine output (populated after consensus is run)",
    )
    mcp_sources: list[dict[str, Any]] = Field(
        default_factory=list,
        description="External data sources used during the meeting (files, spreadsheets, queries, searches)",
    )
    mcp_evidence_summary: Optional[str] = Field(
        default=None,
        description="Structured evidence summary from uploaded MCP data, injected into agent prompts",
    )
