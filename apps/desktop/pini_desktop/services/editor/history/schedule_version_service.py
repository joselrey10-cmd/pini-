import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database


CREATE_SQL = """
CREATE TABLE IF NOT EXISTS schedule_versions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL DEFAULT 'local'
);
"""


@dataclass(frozen=True)
class ScheduleVersion:
    id: int
    name: str
    description: str
    created_at: str
    created_by: str
    sessions_count: int = 0


class ScheduleVersionService:
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

    def create_version(self, name: str, description: str = "", created_by: str = "local") -> int:
        payload = self._read_schedule_payload()
        connection = self._connect()
        try:
            cursor = connection.execute(
                """
                INSERT INTO schedule_versions(name, description, payload, created_at, created_by)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    name.strip() or "Versión sin nombre",
                    description.strip(),
                    json.dumps(payload, ensure_ascii=False),
                    datetime.now().isoformat(timespec="seconds"),
                    created_by,
                ),
            )
            connection.commit()
            return int(cursor.lastrowid)
        finally:
            connection.close()

    def list_versions(self) -> list[ScheduleVersion]:
        connection = self._connect()
        try:
            rows = connection.execute(
                """
                SELECT id, name, description, payload, created_at, created_by
                FROM schedule_versions
                ORDER BY id DESC
                """
            ).fetchall()

            versions = []
            for row in rows:
                payload = json.loads(row["payload"])
                versions.append(
                    ScheduleVersion(
                        id=int(row["id"]),
                        name=row["name"],
                        description=row["description"] or "",
                        created_at=row["created_at"] or "",
                        created_by=row["created_by"] or "local",
                        sessions_count=len(payload.get("sessions", [])),
                    )
                )
            return versions
        finally:
            connection.close()

    def restore_version(self, version_id: int) -> None:
        connection = self._connect()
        try:
            row = connection.execute(
                "SELECT payload FROM schedule_versions WHERE id=?",
                (version_id,),
            ).fetchone()
            if row is None:
                raise ValueError(f"No existe la versión {version_id}")

            payload = json.loads(row["payload"])
            sessions = payload.get("sessions", [])

            connection.execute("DELETE FROM schedule_sessions")
            for session in sessions:
                connection.execute(
                    """
                    INSERT INTO schedule_sessions(
                        id, course_id, subject_id, teacher_id, room_id, day, period
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        session["id"],
                        session["course_id"],
                        session["subject_id"],
                        session["teacher_id"],
                        session["room_id"],
                        session["day"],
                        session["period"],
                    ),
                )
            connection.commit()
        finally:
            connection.close()

    def delete_version(self, version_id: int) -> None:
        connection = self._connect()
        try:
            connection.execute("DELETE FROM schedule_versions WHERE id=?", (version_id,))
            connection.commit()
        finally:
            connection.close()

    def _read_schedule_payload(self) -> dict:
        connection = self._connect()
        try:
            rows = connection.execute(
                """
                SELECT id, course_id, subject_id, teacher_id, room_id, day, period
                FROM schedule_sessions
                ORDER BY day, period, id
                """
            ).fetchall()

            return {
                "sessions": [
                    {
                        "id": int(row["id"]),
                        "course_id": row["course_id"],
                        "subject_id": row["subject_id"],
                        "teacher_id": row["teacher_id"],
                        "room_id": row["room_id"],
                        "day": row["day"],
                        "period": row["period"],
                    }
                    for row in rows
                ]
            }
        finally:
            connection.close()
