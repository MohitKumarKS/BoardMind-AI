"""Spreadsheet MCP Tool.

Reads CSV and Excel files, returning structured data as JSON.
Uses pandas for parsing.
"""

import io
import logging
from typing import Any

logger = logging.getLogger(__name__)


class SpreadsheetTool:
    """Reads spreadsheet files and returns structured data.

    Supports:
    - CSV (.csv)
    - Excel (.xlsx, .xls)
    """

    def read_csv(self, file_path: str | None = None, content: bytes | None = None, max_rows: int = 100) -> dict[str, Any]:
        """Read a CSV file and return structured data.

        Args:
            file_path: Path to a CSV file on disk.
            content: Raw CSV bytes (for uploaded files).
            max_rows: Maximum rows to return (default 100).

        Returns:
            Dict with columns, row_count, preview rows, and summary.
        """
        import pandas as pd

        try:
            if content is not None:
                df = pd.read_csv(io.BytesIO(content))
            elif file_path is not None:
                df = pd.read_csv(file_path)
            else:
                return {"error": "No file path or content provided"}

            return self._dataframe_to_result(df, max_rows, "csv")
        except Exception as e:
            logger.error(f"Spreadsheet CSV read error: {e}")
            return {"error": str(e), "source": "spreadsheet_tool"}

    def read_excel(self, file_path: str | None = None, content: bytes | None = None, sheet_name: str | int = 0, max_rows: int = 100) -> dict[str, Any]:
        """Read an Excel file and return structured data.

        Args:
            file_path: Path to an Excel file on disk.
            content: Raw Excel bytes (for uploaded files).
            sheet_name: Sheet to read (name or index, default first).
            max_rows: Maximum rows to return.

        Returns:
            Dict with columns, row_count, preview rows, and summary.
        """
        import pandas as pd

        try:
            if content is not None:
                df = pd.read_excel(io.BytesIO(content), sheet_name=sheet_name)
            elif file_path is not None:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                return {"error": "No file path or content provided"}

            return self._dataframe_to_result(df, max_rows, "excel")
        except Exception as e:
            logger.error(f"Spreadsheet Excel read error: {e}")
            return {"error": str(e), "source": "spreadsheet_tool"}

    def preview_sheets(self, file_path: str | None = None, content: bytes | None = None) -> dict[str, Any]:
        """List available sheets in an Excel file.

        Returns:
            Dict with sheet names and row counts.
        """
        import pandas as pd

        try:
            if content is not None:
                xls = pd.ExcelFile(io.BytesIO(content))
            elif file_path is not None:
                xls = pd.ExcelFile(file_path)
            else:
                return {"error": "No file path or content provided"}

            sheets = []
            for name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=name, nrows=0)
                sheets.append({"name": name, "columns": list(df.columns)})

            return {"sheets": sheets, "total_sheets": len(sheets)}
        except Exception as e:
            logger.error(f"Spreadsheet preview error: {e}")
            return {"error": str(e), "source": "spreadsheet_tool"}

    def _dataframe_to_result(self, df: Any, max_rows: int, source_type: str) -> dict[str, Any]:
        """Convert a pandas DataFrame to a structured result dict."""
        total_rows = len(df)
        preview_df = df.head(max_rows)

        # Generate summary statistics for numeric columns
        numeric_summary = {}
        for col in df.select_dtypes(include=["number"]).columns:
            numeric_summary[col] = {
                "mean": round(float(df[col].mean()), 2) if not df[col].isna().all() else None,
                "min": round(float(df[col].min()), 2) if not df[col].isna().all() else None,
                "max": round(float(df[col].max()), 2) if not df[col].isna().all() else None,
            }

        return {
            "source": "spreadsheet_tool",
            "source_type": source_type,
            "columns": list(df.columns),
            "total_rows": total_rows,
            "rows_returned": len(preview_df),
            "data": preview_df.to_dict(orient="records"),
            "numeric_summary": numeric_summary,
        }
