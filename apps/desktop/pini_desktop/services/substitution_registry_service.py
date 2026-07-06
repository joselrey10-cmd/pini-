import sqlite3
from dataclasses import dataclass
from datetime import datetime

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database


CREATE_SQL = """
CREATE TABLE IF NOT EXISTS substitution_records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    absent_teacher_id INTEGER NOT NULL,
    substitute_teacher_name TEXT NOT NULL,
    day INTEGER NOT NULL,
    period INTEGER NOT NULL,
    score INTEGER NOT NULL DEFAULT 0,
    reasons TEXT,
    warnings TEXT,
    created_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'PLANNED'
);
"""


@dataclass(frozen=True)
class SubstitutionRecord:
    id: int | None
    absent_teacher_id: int
    substitute_teacher_name: str
    day: int
    period: int
    score: int
    reasons: str = ""
    warnings: str = ""
    created_at: str = ""
    status: str = "PLANNED"


class SubstitutionRegistryService:
    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        initialise_database()
        self._ensure_table()

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _ensure_table(self) -> None:
        con = self._connect()
        try:
            con.executescript(CREATE_SQL)
            con.commit()
        finally:
            con.close()

    def register(
        self,
        absent_teacher_id: int,
        substitute_teacher_name: str,
        day: int,
        period: int,
        score: int,
        reasons: str = "",
        warnings: str = "",
    ) -> int:
        con = self._connect()
        try:
            cursor = con.execute(
                """
                INSERT INTO substitution_records(
                    absent_teacher_id, substitute_teacher_name, day, period,
                    score, reasons, warnings, created_at, status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'PLANNED')
                """,
                (
                    absent_teacher_id,
                    substitute_teacher_name,
                    day,
                    period,
                    score,
                    reasons,
                    warnings,
                    datetime.now().isoformat(timespec="seconds"),
                ),
            )
            con.commit()
            return int(cursor.lastrowid)
        finally:
            con.close()

    def list_records(self) -> list[SubstitutionRecord]:
        con = self._connect()
        try:
            rows = con.execute(
                """
                SELECT * FROM substitution_records
                ORDER BY day, period, created_at DESC
                """
            ).fetchall()
            return [self._row(row) for row in rows]
        finally:
            con.close()

    def mark_done(self, record_id: int) -> None:
        self._set_status(record_id, "DONE")

    def cancel(self, record_id: int) -> None:
        self._set_status(record_id, "CANCELLED")

    def _set_status(self, record_id: int, status: str) -> None:
        con = self._connect()
        try:
            con.execute(
                "UPDATE substitution_records SET status=? WHERE id=?",
                (status, record_id),
            )
            con.commit()
        finally:
            con.close()

    def _row(self, row) -> SubstitutionRecord:
        return SubstitutionRecord(
            id=int(row["id"]),
            absent_teacher_id=int(row["absent_teacher_id"]),
            substitute_teacher_name=row["substitute_teacher_name"],
            day=int(row["day"]),
            period=int(row["period"]),
            score=int(row["score"]),
            reasons=row["reasons"] or "",
            warnings=row["warnings"] or "",
            created_at=row["created_at"] or "",
            status=row["status"] or "PLANNED",
        )
