"""MCP Registry.

Central access point for all MCP tools. Department agents request
tools only through this registry — never importing tool services directly.

The registry also tracks usage: every tool invocation is recorded
so the Board Context and Report Generator can list external data sources.
"""

import logging
from datetime import datetime
from typing import Any

from .spreadsheet.service import SpreadsheetTool
from .filesystem.service import FilesystemTool
from .database.service import DatabaseTool
from .websearch.service import WebSearchTool

logger = logging.getLogger(__name__)


class MCPRegistry:
    """Central registry for MCP tools with usage tracking.

    Provides lazy-initialized tool instances. Each tool is created
    on first access and reused thereafter. Every data retrieval
    is recorded in the usage log for reporting.

    Usage:
        registry = MCPRegistry()
        data = registry.read_spreadsheet(content=csv_bytes, filename="sales.csv")
        text = registry.read_file(content=pdf_bytes, filename="report.pdf")
        results = registry.search_web("market trends AI")
        rows = registry.query_database("SELECT * FROM sales", db_path="data.db")
    """

    def __init__(self):
        self._spreadsheet: SpreadsheetTool | None = None
        self._filesystem: FilesystemTool | None = None
        self._database: DatabaseTool | None = None
        self._websearch: WebSearchTool | None = None
        self._usage_log: list[dict[str, Any]] = []

    @property
    def usage_log(self) -> list[dict[str, Any]]:
        """All recorded MCP tool usage entries."""
        return self._usage_log

    def clear_usage_log(self) -> None:
        """Clear the usage log (e.g. between sessions)."""
        self._usage_log = []

    # --- Tool accessors (for direct low-level access) ---

    def get_spreadsheet_tool(self) -> SpreadsheetTool:
        """Get the spreadsheet tool (CSV/Excel reader)."""
        if self._spreadsheet is None:
            self._spreadsheet = SpreadsheetTool()
        return self._spreadsheet

    def get_filesystem_tool(self) -> FilesystemTool:
        """Get the filesystem tool (text/PDF/DOCX reader)."""
        if self._filesystem is None:
            self._filesystem = FilesystemTool()
        return self._filesystem

    def get_database_tool(self) -> DatabaseTool:
        """Get the database tool (read-only SQL queries)."""
        if self._database is None:
            self._database = DatabaseTool()
        return self._database

    def get_websearch_tool(self) -> WebSearchTool:
        """Get the web search tool."""
        if self._websearch is None:
            self._websearch = WebSearchTool()
        return self._websearch

    # --- High-level tracked operations ---

    def read_spreadsheet(
        self,
        content: bytes | None = None,
        file_path: str | None = None,
        filename: str = "unknown.csv",
        max_rows: int = 100,
    ) -> dict[str, Any]:
        """Read a spreadsheet via MCP and record usage."""
        tool = self.get_spreadsheet_tool()
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "csv"

        if ext in ("xlsx", "xls"):
            result = tool.read_excel(file_path=file_path, content=content, max_rows=max_rows)
        else:
            result = tool.read_csv(file_path=file_path, content=content, max_rows=max_rows)

        self._record_usage("spreadsheet", filename, result)
        return result

    def read_file(
        self,
        content: bytes | None = None,
        file_path: str | None = None,
        filename: str = "unknown.txt",
    ) -> dict[str, Any]:
        """Read a file via MCP and record usage."""
        tool = self.get_filesystem_tool()
        result = tool.read_file(file_path=file_path, content=content, filename=filename)
        self._record_usage("filesystem", filename, result)
        return result

    def query_database(
        self,
        sql: str,
        db_path: str = ":memory:",
        max_rows: int = 100,
    ) -> dict[str, Any]:
        """Execute a database query via MCP and record usage."""
        tool = self.get_database_tool()
        result = tool.query(sql=sql, db_path=db_path, max_rows=max_rows)
        self._record_usage("database", f"query: {sql[:80]}", result)
        return result

    def search_web(self, query: str, max_results: int = 5) -> dict[str, Any]:
        """Search the web via MCP and record usage."""
        tool = self.get_websearch_tool()
        result = tool.search(query=query, max_results=max_results)
        self._record_usage("websearch", f"search: {query[:80]}", result)
        return result

    def _record_usage(self, tool_type: str, resource: str, result: dict[str, Any]) -> None:
        """Record a tool usage entry."""
        entry = {
            "tool_type": tool_type,
            "resource": resource,
            "timestamp": datetime.utcnow().isoformat(),
            "success": "error" not in result,
        }

        # Add metadata depending on tool type
        if tool_type == "spreadsheet":
            entry["rows"] = result.get("total_rows")
            entry["columns"] = result.get("columns")
        elif tool_type == "filesystem":
            entry["format"] = result.get("format")
            entry["chars"] = result.get("char_count")
        elif tool_type == "database":
            entry["rows_returned"] = result.get("total_rows_returned")
        elif tool_type == "websearch":
            entry["result_count"] = result.get("result_count")

        self._usage_log.append(entry)
        logger.info(f"MCP usage recorded: {tool_type} — {resource}")
