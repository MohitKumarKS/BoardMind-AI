"""Executive Report schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DepartmentEntry(BaseModel):
    """Summary of one department's participation."""

    agent_id: str
    position: str
    confidence: float
    summary: str


class ConsensusSection(BaseModel):
    """Consensus summary for the report."""

    decision: str
    confidence: float
    support_count: int
    conditional_count: int
    neutral_count: int
    oppose_count: int
    conflict_detected: bool
    executive_summary: str


class MeetingStatistics(BaseModel):
    """Execution statistics."""

    total_departments: int
    departments_completed: int
    departments_failed: int
    total_execution_time_ms: int
    session_id: str


class ExternalDataSource(BaseModel):
    """An external data source used during the meeting."""

    tool_type: str = Field(..., description="Type: spreadsheet | filesystem | database | websearch")
    resource: str = Field(..., description="Resource identifier (filename, query, etc.)")
    timestamp: str = Field(..., description="When the source was accessed")
    success: bool = Field(default=True, description="Whether the extraction succeeded")
    metadata: dict = Field(default_factory=dict, description="Additional source metadata")


class ExecutiveReport(BaseModel):
    """Complete structured executive report."""

    title: str = Field(default="Executive Decision Report")
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    scenario: str
    business_category: str
    final_decision: str
    consensus_confidence: float
    departments: list[DepartmentEntry]
    consensus: ConsensusSection
    key_risks: list[str]
    recommended_actions: list[str]
    statistics: MeetingStatistics
    external_data_sources: list[ExternalDataSource] = Field(
        default_factory=list,
        description="External data sources used during the meeting (populated when MCP was used)",
    )
