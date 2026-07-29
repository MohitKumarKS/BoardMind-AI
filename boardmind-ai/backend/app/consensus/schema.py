"""Consensus Engine request schema."""

from pydantic import BaseModel, Field


class ConsensusRequest(BaseModel):
    """Request to run the Consensus Engine on an existing session."""

    session_id: str = Field(
        ...,
        description="The session ID of a completed orchestration to analyze",
    )
