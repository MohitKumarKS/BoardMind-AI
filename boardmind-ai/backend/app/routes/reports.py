"""Executive Report API route.

Provides endpoints for generating and downloading executive reports
in JSON and PDF formats. Also persists reports to PostgreSQL.
"""

import base64
import logging

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

from app.reports import ReportGeneratorService, ExecutiveReport
from app.routes.boardroom import orchestrator

logger = logging.getLogger(__name__)

router = APIRouter()

report_service = ReportGeneratorService(orchestrator.board_context)


@router.get("/{session_id}")
async def get_report(
    session_id: str,
    format: str = Query(default="json", description="Report format: json or pdf"),
):
    """Generate and return an executive report for a completed session.

    Supports two formats:
    - json: Returns the structured report as JSON
    - pdf: Returns a downloadable PDF file

    The session must have a completed consensus result.
    Reports are also persisted to PostgreSQL for history.
    """
    try:
        if format == "pdf":
            pdf_bytes = report_service.generate_pdf(session_id)

            # Persist to PostgreSQL (non-blocking)
            await _persist_report(session_id)

            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename=boardmind-report-{session_id[:8]}.pdf"
                },
            )
        else:
            report = report_service.generate(session_id)

            # Persist to PostgreSQL (non-blocking)
            await _persist_report(session_id)

            return report.model_dump(mode="json")

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ImportError as e:
        raise HTTPException(
            status_code=501,
            detail=f"PDF generation requires fpdf2. Install with: pip install fpdf2. Error: {e}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Report generation failed: {str(e)}",
        )


async def _persist_report(session_id: str):
    """Save report JSON + PDF to PostgreSQL for history."""
    try:
        from app.mcp_hub.database import is_database_ready
        if not is_database_ready():
            return

        from app.mcp_hub.storage_service import StorageService

        report = report_service.generate(session_id)
        pdf_bytes = report_service.generate_pdf(session_id)

        report_json = report.model_dump(mode="json")
        pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")

        storage = StorageService()
        await storage.store_report(session_id, report_json, pdf_b64)

    except Exception as e:
        logger.debug(f"Report persistence skipped: {e}")
