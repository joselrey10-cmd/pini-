import json
import sqlite3
from dataclasses import dataclass

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database


@dataclass(frozen=True)
class ScheduleVersionComparison:
    first_id: int
    second_id: int
    first_sessions: int
    second_sessions: int
    added: int
    removed: int
    moved: int
    summary: str


class ScheduleVersionComparator:
    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        initialise_database(database_path=self.database_path)

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def compare(self, first_id: int, second_id: int) -> ScheduleVersionComparison:
        first = self._load_payload(first_id)
        second = self._load_payload(second_id)

        first_map = {item["id"]: item for item in first.get("sessions", [])}
        second_map = {item["id"]: item for item in second.get("sessions", [])}

        added_ids = set(second_map) - set(first_map)
        removed_ids = set(first_map) - set(second_map)

        moved = 0
        for session_id in set(first_map).intersection(second_map):
            a = first_map[session_id]
            b = second_map[session_id]
            if a.get("day") != b.get("day") or a.get("period") != b.get("period"):
                moved += 1

        summary = (
            f"Comparación {first_id} → {second_id}: "
            f"{len(added_ids)} añadidas, {len(removed_ids)} eliminadas, {moved} movidas."
        )

        return ScheduleVersionComparison(
            first_id=first_id,
            second_id=second_id,
            first_sessions=len(first_map),
            second_sessions=len(second_map),
            added=len(added_ids),
            removed=len(removed_ids),
            moved=moved,
            summary=summary,
        )

    def _load_payload(self, version_id: int) -> dict:
        connection = self._connect()
        try:
            row = connection.execute(
                "SELECT payload FROM schedule_versions WHERE id=?",
                (version_id,),
            ).fetchone()
            if row is None:
                raise ValueError(f"No existe la versión {version_id}")
            return json.loads(row["payload"])
        finally:
            connection.close()
