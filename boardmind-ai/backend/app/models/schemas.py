"""Pydantic models for BoardMind AI shared types."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Position(str, Enum):
    SUPPORT = "support"
    OPPOSE = "oppose"
    NEUTRAL = "neutral"
    CONDITIONAL = "conditional"


class ConsensusLevel(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    SPLIT = "split"
    NONE = "none"


class SessionStatus(str, Enum):
    CREATED = "created"
    ROUND_1_ACTIVE = "round_1_active"
    ROUND_1_COMPLETE = "round_1_complete"
    ROUND_2_ACTIVE = "round_2_active"
    ROUND_2_COMPLETE = "round_2_complete"
    ROUND_3_ACTIVE = "round_3_active"
    ROUND_3_COMPLETE = "round_3_complete"
    SYNTHESIZING = "synthesizing"
    COMPLETED = "completed"
    ERROR = "error"


class AgentIdentity(BaseModel):
    agent_id: str
    title: str
    short: str
    domain: str
    color: str


class AgentResponse(BaseModel):
    agent_id: str
    round: int
    position: Position
    confidence: float
    domain_assessment: dict
    summary: str
    rationale: str
    risks: list[str]
    conditions: list[str]
    references_to: list[str] = []


class SessionCreate(BaseModel):
    scenario: str
    mode: str = "boardroom"  # "workspace" or "boardroom"
    agents: list[str] = []  # empty = all agents


class SessionResponse(BaseModel):
    session_id: str
    scenario: str
    mode: str
    status: SessionStatus
    participating_agents: list[str]
    current_round: int = 0


class ConsensusResult(BaseModel):
    consensus_score: float
    consensus_level: ConsensusLevel
    executive_summary: str
    key_agreements: list[str]
    key_disagreements: list[str]
    dissenting_views: list[dict]
    risk_matrix: list[dict]
    recommended_next_steps: list[str]


class ReportResponse(BaseModel):
    report_id: str
    session_id: str
    content: str
    format: str = "markdown"
