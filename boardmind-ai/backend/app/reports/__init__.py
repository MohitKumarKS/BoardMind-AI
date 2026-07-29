"""Executive Report Generator module.

Produces professional executive reports from Board Context sessions.
Supports JSON and PDF formats. Includes External Data Sources section
when MCP tools were used during the meeting.

Usage:
    from app.reports import ReportGeneratorService

    service = ReportGeneratorService(board_context)
    report = service.generate(session_id)
    pdf_bytes = service.generate_pdf(session_id)
"""

from .schema import ExecutiveReport, DepartmentEntry, ConsensusSection, MeetingStatistics, ExternalDataSource
from .service import ReportGeneratorService

__all__ = [
    "ReportGeneratorService",
    "ExecutiveReport",
    "DepartmentEntry",
    "ConsensusSection",
    "MeetingStatistics",
    "ExternalDataSource",
]
