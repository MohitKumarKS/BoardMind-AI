"""MCP (Model Context Protocol) layer.

Provides external data tools to department agents via a central registry.
All tools are optional — agents work without MCP when no external data is provided.

Usage:
    from app.mcp import MCPRegistry

    registry = MCPRegistry()
    data = registry.get_spreadsheet_tool().read_csv("path/to/file.csv")
    text = registry.get_filesystem_tool().read_file("path/to/doc.pdf")
    results = registry.get_database_tool().query("SELECT * FROM sales LIMIT 10")
    search = registry.get_websearch_tool().search("market trends AI 2024")
"""

from .registry import MCPRegistry

__all__ = ["MCPRegistry"]
