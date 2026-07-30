"""SQLAlchemy ORM models for the MCP Knowledge Hub.

Normalized PostgreSQL schema:
- Meeting: board meeting sessions
- ExecutiveAnalysis: per-agent analysis results
- ConsensusRecord: final board decisions
- Evidence: domain-specific evidence stored for retrieval
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column, String, Integer, Float, Text, DateTime, Boolean,
    ForeignKey, JSON, Index
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Meeting(Base):
    """A board meeting session."""
    __tablename__ = "meetings"

    meeting_id = Column(String(64), primary_key=True)
    title = Column(String(500), nullable=True)
    proposal = Column(Text, nullable=False)
    business_category = Column(String(100), nullable=True)
    optional_context = Column(Text, nullable=True)
    report_json = Column(JSON, nullable=True)  # Full report content
    report_pdf = Column(Text, nullable=True)  # Base64-encoded PDF
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    analyses = relationship("ExecutiveAnalysis", back_populates="meeting", cascade="all, delete-orphan")
    consensus = relationship("ConsensusRecord", back_populates="meeting", uselist=False, cascade="all, delete-orphan")


class ExecutiveAnalysis(Base):
    """A single executive agent's analysis for a meeting."""
    __tablename__ = "executive_analyses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    meeting_id = Column(String(64), ForeignKey("meetings.meeting_id"), nullable=False)
    executive_role = Column(String(50), nullable=False)
    recommendation = Column(String(20), nullable=False)  # support/oppose/neutral/conditional
    confidence = Column(Float, nullable=False)
    rationale = Column(Text, nullable=True)
    risks = Column(JSON, nullable=True)
    supporting_conditions = Column(JSON, nullable=True)
    recommended_actions = Column(JSON, nullable=True)
    execution_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    meeting = relationship("Meeting", back_populates="analyses")

    __table_args__ = (
        Index("ix_exec_analysis_meeting", "meeting_id"),
        Index("ix_exec_analysis_role", "executive_role"),
    )


class ConsensusRecord(Base):
    """Final consensus decision for a meeting."""
    __tablename__ = "consensus_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    meeting_id = Column(String(64), ForeignKey("meetings.meeting_id"), nullable=False, unique=True)
    decision = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    summary = Column(Text, nullable=True)
    votes = Column(JSON, nullable=True)  # {support: N, conditional: N, ...}
    participating_agents = Column(JSON, nullable=True)
    conflict_detected = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    meeting = relationship("Meeting", back_populates="consensus")

    __table_args__ = (
        Index("ix_consensus_decision", "decision"),
    )


class Evidence(Base):
    """Stored evidence for domain-specific retrieval."""
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(200), nullable=False)  # file, api, database, manual
    category = Column(String(100), nullable=False)  # finance, legal, it, etc.
    content = Column(Text, nullable=False)
    extra_metadata = Column("metadata", JSON, nullable=True)
    meeting_id = Column(String(64), nullable=True)  # optional link to meeting
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_evidence_category", "category"),
        Index("ix_evidence_source", "source"),
    )
