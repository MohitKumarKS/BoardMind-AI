"""Database MCP Tool.

Provides read-only SQL query execution.
Currently supports SQLite. Designed for future extension
to PostgreSQL, MySQL, Snowflake without interface changes.
"""

import logging
import sqlite3
from typing import Any

logger = logging.getLogger(__name__)


class DatabaseTool:
    """Executes read-only SQL queries against databases.

    Currently supports:
    - SQLite (local file or in-memory)

    Future support (same interface):
    - PostgreSQL
    - MySQL
    - Snowflake
    """

    def query(
        self,
        sql: str,
        db_path: str = ":memory:",
        max_rows: int = 100,
    ) -> dict[str, Any]:
        """Execute a read-only SQL query.

        Args:
            sql: SQL query to execute (must be SELECT or read-only).
            db_path: Path to SQLite database file (default: in-memory).
            max_rows: Maximum rows to return.

        Returns:
            Dict with columns, data rows, row count, and metadata.
        """
        # Security: only allow read operations
        sql_upper = sql.strip().upper()
        if not any(sql_upper.startswith(kw) for kw in ("SELECT", "PRAGMA", "EXPLAIN", "WITH")):
            return {
                "error": "Only SELECT queries are allowed (read-only access)",
                "source": "database_tool",
            }

        # Block dangerous operations even in subqueries
        dangerous = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE"]
        for keyword in dangerous:
            if keyword in sql_upper:
                return {
                    "error": f"Query contains forbidden keyword: {keyword}",
                    "source": "database_tool",
                }

        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(sql)

            rows = cursor.fetchmany(max_rows)
            columns = [desc[0] for desc in cursor.description] if cursor.description else []

            data = [dict(row) for row in rows]
            total_available = cursor.fetchone() is not None  # Check if more rows exist

            conn.close()

            return {
                "source": "database_tool",
                "database": db_path,
                "columns": columns,
                "total_rows_returned": len(data),
                "has_more_rows": total_available,
                "data": data,
            }
        except sqlite3.Error as e:
            logger.error(f"Database query error: {e}")
            return {"error": f"SQLite error: {e}", "source": "database_tool"}
        except Exception as e:
            logger.error(f"Database tool error: {e}")
            return {"error": str(e), "source": "database_tool"}

    def list_tables(self, db_path: str) -> dict[str, Any]:
        """List all tables in a SQLite database.

        Args:
            db_path: Path to the SQLite database.

        Returns:
            Dict with table names and their columns.
        """
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = [row[0] for row in cursor.fetchall()]

            table_info = []
            for table in tables:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [{"name": row[1], "type": row[2]} for row in cursor.fetchall()]
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                row_count = cursor.fetchone()[0]
                table_info.append({
                    "name": table,
                    "columns": columns,
                    "row_count": row_count,
                })

            conn.close()

            return {
                "source": "database_tool",
                "database": db_path,
                "tables": table_info,
                "total_tables": len(tables),
            }
        except Exception as e:
            logger.error(f"Database list_tables error: {e}")
            return {"error": str(e), "source": "database_tool"}
