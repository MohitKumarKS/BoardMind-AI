"""MCP file upload and data extraction API routes.

Provides endpoint for uploading files that are processed through
MCP tools and returned as structured data for agent consumption.
All operations are tracked via the registry's usage log.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Any

from app.mcp import MCPRegistry
from app.mcp.summarizer import summarize_mcp_data

router = APIRouter()

registry = MCPRegistry()

# Per-session evidence storage (keyed by a rotating slot).
# This replaces the previous global _last_evidence_summary which was a race condition.
# A proper fix would use request-scoped context, but for the hackathon,
# we use a dict keyed by a simple counter to avoid cross-request overwrite.
import threading

_evidence_lock = threading.Lock()
_evidence_store: dict[int, str] = {}
_evidence_counter: int = 0

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".txt", ".md", ".pdf", ".docx"}
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB limit


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> dict[str, Any]:
    """Upload a file and extract its contents via MCP tools.

    Supports: CSV, Excel, PDF, DOCX, TXT, Markdown
    Max size: 10MB

    Returns structured data extracted from the file, ready for
    consumption by department agents. Usage is tracked in the registry.
    Also generates and stores an evidence summary for agent injection.
    """
    global _evidence_counter

    filename = file.filename or "unknown"
    ext = ("." + filename.rsplit(".", 1)[-1].lower()) if "." in filename else ""

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: '{ext}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    content = await file.read()

    if len(content) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({len(content)} bytes). Maximum: {MAX_UPLOAD_SIZE} bytes (10MB).",
        )

    if ext in (".csv", ".xlsx", ".xls"):
        result = registry.read_spreadsheet(content=content, filename=filename)
    else:
        result = registry.read_file(content=content, filename=filename)

    result["filename"] = filename
    result["file_size_bytes"] = len(content)

    # Generate structured evidence summary
    evidence_summary = summarize_mcp_data(result)
    with _evidence_lock:
        _evidence_counter += 1
        _evidence_store[_evidence_counter] = evidence_summary
    result["evidence_summary"] = evidence_summary

    return result


def get_registry() -> MCPRegistry:
    """Expose the module-level registry for use by other routes."""
    return registry


def get_and_clear_evidence_summary() -> str:
    """Get the most recent evidence summary and clear it.
    
    Called by the boardroom route after orchestration to store
    the summary in Board Context. Thread-safe.
    """
    with _evidence_lock:
        if not _evidence_store:
            return ""
        # Get the latest entry
        latest_key = max(_evidence_store.keys())
        summary = _evidence_store.pop(latest_key, "")
        return summary
