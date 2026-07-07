import sqlite3
from dataclasses import dataclass
from datetime import datetime

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database


CREATE_SQL = """
CREATE TABLE IF NOT EXISTS editor_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    success INTEGER NOT NULL DEFAULT 0,
    messages TEXT,
    warnings TEXT,
    old_score REAL,
    new_score REAL,
    created_at TEXT NOT NULL
);
"""


@dataclass(frozen=True)
class EditorHistoryRecord:
    id: int
    action: str
    success: bool
    messages: str = ""
    warnings: str = ""
    old_score: float | None = None
    new_score: float | None = None
    created_at: str = ""


class EditorHistoryService:
    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        initialise_database(database_path=self.database_path)
        self._ensure_table()

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _ensure_table(self):
        connection = self._connect()
        try:
            connection.executescript(CREATE_SQL)
            connection.commit()
        finally:
            connection.close()

    def record_result(self, action: str, result) -> int:
        messages = "\n".join(getattr(result, "messages", ()) or ())
        warnings = "\n".join(getattr(result, "warnings", ()) or ())
        old_score = getattr(result, "old_score", None)
        new_score = getattr(result, "new_score", None)

        connection = self._connect()
        try:
            cursor = connection.execute(
                """
                INSERT INTO editor_history(action, success, messages, warnings, old_score, new_score, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    action,
                    1 if getattr(result, "success", False) else 0,
                    messages,
                    warnings,
                    old_score,
                    new_score,
                    datetime.now().isoformat(timespec="seconds"),
                ),
            )
            connection.commit()
            return int(cursor.lastrowid)
        finally:
            connection.close()

    def list_records(self, limit: int = 100) -> list[EditorHistoryRecord]:
        connection = self._connect()
        try:
            rows = connection.execute(
                """
                SELECT * FROM editor_history
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

            return [
                EditorHistoryRecord(
                    id=int(row["id"]),
                    action=row["action"],
                    success=bool(row["success"]),
                    messages=row["messages"] or "",
                    warnings=row["warnings"] or "",
                    old_score=row["old_score"],
                    new_score=row["new_score"],
                    created_at=row["created_at"] or "",
                )
                for row in rows
            ]
        finally:
            connection.close()

    def clear(self) -> None:
        connection = self._connect()
        try:
            connection.execute("DELETE FROM editor_history")
            connection.commit()
        finally:
            connection.close()
