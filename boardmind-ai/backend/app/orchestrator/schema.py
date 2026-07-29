"""Executive Orchestrator request and response schemas."""

from typing import Optional, Any

from pydantic import BaseModel, Field


class OrchestratorRequest(BaseModel):
    """Input request for the Executive Orchestrator."""

    scenario: str = Field(
        ...,
        min_length=20,
        description="The business scenario to analyze across multiple departments",
        examples=[
            "We are considering launching a new AI-powered analytics product "
            "targeting mid-market companies at $2,000/month."
        ],
    )
    optional_context: Optional[str] = Field(
        default=None,
        description="Additional context or constraints for all agents",
    )


class AgentExecutionResult(BaseModel):
    """Result of a single agent's execution within the orchestration."""

    agent_id: str = Field(
        ..., description="The department agent identifier"
    )
    response: Optional[dict[str, Any]] = Field(
        default=None,
        description="The agent's full structured response (null if failed)",
    )
    execution_time_ms: int = Field(
        ..., description="Time taken for this agent's execution in milliseconds"
    )
    status: str = Field(
        ...,
        description="Execution status: completed | failed | timeout",
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message if the agent failed",
    )


class ExecutionSummary(BaseModel):
    """Summary of the orchestration execution."""

    total_agents_selected: int = Field(
        ..., description="Number of agents selected by the Decision Router"
    )
    total_agents_completed: int = Field(
        ..., description="Number of agents that completed successfully"
    )
    total_agents_failed: int = Field(
        default=0, description="Number of agents that failed"
    )
    total_execution_time_ms: int = Field(
        ..., description="Total wall-clock time for all agents (parallel)"
    )


class OrchestratorResponse(BaseModel):
    """Output response from the Executive Orchestrator."""

    session_id: str = Field(
        ..., description="Unique identifier for this orchestration session"
    )
    scenario: str = Field(
        ..., description="The original business scenario"
    )
    business_category: str = Field(
        ..., description="The category determined by the Decision Router"
    )
    selected_agents: list[str] = Field(
        ..., description="Agents selected by the Decision Router"
    )
    execution_summary: ExecutionSummary = Field(
        ..., description="Summary of execution results"
    )
    responses: list[AgentExecutionResult] = Field(
        ..., description="Individual agent execution results"
    )
