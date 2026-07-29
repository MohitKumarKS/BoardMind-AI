"""Executive Report Generator service.

Produces professional reports from completed Board Context sessions.
Supports JSON and PDF output formats. No LLM calls.
"""

import io
import logging
from datetime import datetime

from app.board_context import BoardContextService, BoardContext

from .schema import (
    ExecutiveReport,
    DepartmentEntry,
    ConsensusSection,
    MeetingStatistics,
    ExternalDataSource,
)

logger = logging.getLogger(__name__)


class ReportGeneratorService:
    """Generates executive reports from Board Context.

    Usage:
        service = ReportGeneratorService(board_context)
        report = service.generate(session_id)
        pdf_bytes = service.generate_pdf(session_id)
    """

    def __init__(self, board_context: BoardContextService):
        self._board_context = board_context

    def generate(self, session_id: str) -> ExecutiveReport:
        """Generate a structured executive report.

        Args:
            session_id: The completed board session to report on.

        Returns:
            ExecutiveReport with all sections populated.

        Raises:
            ValueError: If session not found or consensus not available.
        """
        context = self._board_context.get_context(session_id)
        if not context:
            raise ValueError(f"Session '{session_id}' not found")

        if not context.consensus_result:
            raise ValueError(
                f"Session '{session_id}' has no consensus result. "
                f"Run consensus before generating report."
            )

        departments = self._build_departments(context)
        consensus = self._build_consensus_section(context)
        statistics = self._build_statistics(context)
        external_sources = self._build_external_sources(context)

        return ExecutiveReport(
            generated_at=datetime.utcnow(),
            scenario=context.scenario,
            business_category=context.business_category.replace("_", " ").title(),
            final_decision=context.consensus_result.decision.replace("_", " ").title(),
            consensus_confidence=context.consensus_result.confidence,
            departments=departments,
            consensus=consensus,
            key_risks=context.consensus_result.key_risks,
            recommended_actions=context.consensus_result.recommended_actions,
            statistics=statistics,
            external_data_sources=external_sources,
        )

    def generate_pdf(self, session_id: str) -> bytes:
        """Generate a PDF executive report.

        Args:
            session_id: The completed board session.

        Returns:
            PDF file as bytes.
        """
        report = self.generate(session_id)
        return self._render_pdf(report)

    def _build_departments(self, context: BoardContext) -> list[DepartmentEntry]:
        """Extract department summaries from agent results."""
        entries = []

        for agent_id, result in context.agent_results.items():
            if result.status != "completed" or result.response is None:
                continue

            response = result.response
            raw_pos = str(response.get("position", "neutral"))
            position = raw_pos.split(".")[-1].lower() if "." in raw_pos else raw_pos.lower()
            confidence = float(response.get("confidence", 0))
            summary = str(response.get("summary", "No summary available"))

            entries.append(DepartmentEntry(
                agent_id=agent_id,
                position=position,
                confidence=confidence,
                summary=summary,
            ))

        return entries

    def _build_consensus_section(self, context: BoardContext) -> ConsensusSection:
        """Build the consensus section from stored result."""
        cr = context.consensus_result
        assert cr is not None

        return ConsensusSection(
            decision=cr.decision.replace("_", " ").title(),
            confidence=cr.confidence,
            support_count=cr.support_count,
            conditional_count=cr.conditional_count,
            neutral_count=cr.neutral_count,
            oppose_count=cr.oppose_count,
            conflict_detected=cr.conflict_detected,
            executive_summary=cr.executive_summary,
        )

    def _build_statistics(self, context: BoardContext) -> MeetingStatistics:
        """Build meeting statistics section."""
        return MeetingStatistics(
            total_departments=context.execution_metadata.total_agents,
            departments_completed=context.execution_metadata.completed_agents,
            departments_failed=context.execution_metadata.failed_agents,
            total_execution_time_ms=context.execution_metadata.total_execution_time_ms,
            session_id=context.session_id,
        )

    def _build_external_sources(self, context: BoardContext) -> list[ExternalDataSource]:
        """Build external data sources section from Board Context MCP sources."""
        sources = []
        for entry in context.mcp_sources:
            metadata = {}
            for key in ("rows", "columns", "format", "chars", "rows_returned", "result_count"):
                if key in entry:
                    metadata[key] = entry[key]

            sources.append(ExternalDataSource(
                tool_type=entry.get("tool_type", "unknown"),
                resource=entry.get("resource", "unknown"),
                timestamp=entry.get("timestamp", ""),
                success=entry.get("success", True),
                metadata=metadata,
            ))
        return sources

    @staticmethod
    def _sanitize(text: str) -> str:
        """Sanitize text for PDF rendering (latin-1 safe)."""
        replacements = {
            "\u2014": "-",  # em dash
            "\u2013": "-",  # en dash
            "\u2018": "'",  # left single quote
            "\u2019": "'",  # right single quote
            "\u201c": '"',  # left double quote
            "\u201d": '"',  # right double quote
            "\u2026": "...",  # ellipsis
            "\u2022": "-",  # bullet
            "\u00a0": " ",  # non-breaking space
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        # Strip any remaining non-latin1 characters
        return text.encode("latin-1", errors="replace").decode("latin-1")

    def _render_pdf(self, report: ExecutiveReport) -> bytes:
        """Render an ExecutiveReport to PDF bytes using fpdf2."""
        from fpdf import FPDF

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.add_page()

        # Title
        pdf.set_font("Helvetica", "B", 22)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(0, 12, "BoardMind AI", new_x="LMARGIN", new_y="NEXT", align="C")

        pdf.set_font("Helvetica", "", 14)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(0, 8, "Executive Decision Report", new_x="LMARGIN", new_y="NEXT", align="C")

        pdf.set_font("Helvetica", "", 9)
        pdf.cell(
            0, 6,
            f"Generated: {report.generated_at.strftime('%B %d, %Y at %H:%M UTC')}",
            new_x="LMARGIN", new_y="NEXT", align="C",
        )
        pdf.ln(10)

        # Section 1: Executive Summary
        self._pdf_section_header(pdf, "1. Executive Summary")
        self._pdf_key_value(pdf, "Business Scenario", self._sanitize(report.scenario))
        self._pdf_key_value(pdf, "Business Category", self._sanitize(report.business_category))
        self._pdf_key_value(pdf, "Final Decision", self._sanitize(report.final_decision))
        self._pdf_key_value(pdf, "Consensus Confidence", f"{report.consensus_confidence * 100:.0f}%")
        pdf.ln(6)

        # Section 2: Participating Departments
        self._pdf_section_header(pdf, "2. Participating Departments")

        # Table header
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_fill_color(241, 245, 249)
        pdf.cell(45, 7, "Department", border=1, fill=True)
        pdf.cell(25, 7, "Position", border=1, fill=True)
        pdf.cell(20, 7, "Confidence", border=1, fill=True)
        pdf.cell(0, 7, "Summary", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "", 8)
        for dept in report.departments:
            dept_name = dept.agent_id.replace("_", " ").title()
            summary_short = dept.summary[:80] + "..." if len(dept.summary) > 80 else dept.summary

            pdf.cell(45, 6, self._sanitize(dept_name), border=1)
            pdf.cell(25, 6, dept.position.title(), border=1)
            pdf.cell(20, 6, f"{dept.confidence * 100:.0f}%", border=1)
            pdf.cell(0, 6, self._sanitize(summary_short), border=1, new_x="LMARGIN", new_y="NEXT")

        pdf.ln(6)

        # Section 3: Consensus
        self._pdf_section_header(pdf, "3. Consensus")
        self._pdf_key_value(pdf, "Decision", self._sanitize(report.consensus.decision))
        self._pdf_key_value(
            pdf, "Votes",
            f"Support: {report.consensus.support_count} | "
            f"Conditional: {report.consensus.conditional_count} | "
            f"Neutral: {report.consensus.neutral_count} | "
            f"Oppose: {report.consensus.oppose_count}",
        )
        self._pdf_key_value(pdf, "Conflict Detected", "Yes" if report.consensus.conflict_detected else "No")
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(0, 5, self._sanitize(report.consensus.executive_summary))
        pdf.ln(6)

        # Section 4: Key Risks
        if report.key_risks:
            self._pdf_section_header(pdf, "4. Key Risks")
            for risk in report.key_risks[:10]:
                self._pdf_bullet(pdf, risk)
            pdf.ln(6)

        # Section 5: Recommended Actions
        if report.recommended_actions:
            self._pdf_section_header(pdf, "5. Recommended Actions")
            for action in report.recommended_actions[:10]:
                self._pdf_bullet(pdf, action)
            pdf.ln(6)

        # Section 6: Meeting Statistics
        self._pdf_section_header(pdf, "6. Meeting Statistics")
        self._pdf_key_value(pdf, "Total Departments", str(report.statistics.total_departments))
        self._pdf_key_value(pdf, "Departments Completed", str(report.statistics.departments_completed))
        self._pdf_key_value(pdf, "Departments Failed", str(report.statistics.departments_failed))
        self._pdf_key_value(pdf, "Total Execution Time", f"{report.statistics.total_execution_time_ms}ms")
        self._pdf_key_value(pdf, "Session ID", report.statistics.session_id)

        # Section 7: External Data Sources (if any MCP sources were used)
        if report.external_data_sources:
            pdf.ln(6)
            self._pdf_section_header(pdf, "7. External Data Sources")
            for src in report.external_data_sources:
                status = "OK" if src.success else "FAILED"
                line = f"[{src.tool_type.upper()}] {src.resource} ({status})"
                if src.metadata:
                    details = ", ".join(f"{k}={v}" for k, v in src.metadata.items() if v is not None)
                    if details:
                        line += f" - {details}"
                self._pdf_bullet(pdf, line)

        return bytes(pdf.output())

    def _pdf_section_header(self, pdf: "FPDF", title: str) -> None:
        """Render a section header."""
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(226, 232, 240)
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 170, pdf.get_y())
        pdf.ln(4)
        pdf.set_text_color(51, 65, 85)

    def _pdf_key_value(self, pdf: "FPDF", key: str, value: str) -> None:
        """Render a key-value pair."""
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(0, 5, f"{key}:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(0, 5, self._sanitize(value))
        pdf.ln(1)

    def _pdf_bullet(self, pdf: "FPDF", text: str) -> None:
        """Render a bullet point."""
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(5, 4, "-", new_x="RIGHT")
        pdf.multi_cell(0, 4, self._sanitize(text))
        pdf.ln(1)
