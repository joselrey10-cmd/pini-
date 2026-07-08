import sqlite3
from dataclasses import dataclass

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database
from pini_desktop.services.editor.optimization.zone_definition import ZoneDefinition

@dataclass(frozen=True)
class ZoneSession:
    id: int
    day: int
    period: int
    course_id: int | None
    teacher_id: int | None
    room_id: int | None

class ZoneCandidateProvider:
    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        initialise_database(database_path=self.database_path)

    def _connect(self):
        con = sqlite3.connect(self.database_path)
        con.row_factory = sqlite3.Row
        return con

    def list_sessions(self, zone: ZoneDefinition) -> tuple[ZoneSession, ...]:
        where, params = self._where(zone)
        con = self._connect()
        try:
            rows = con.execute(
                f"SELECT id, day, period, course_id, teacher_id, room_id FROM schedule_sessions WHERE {where} ORDER BY day, period, id",
                params,
            ).fetchall()
            return tuple(
                ZoneSession(int(r["id"]), int(r["day"]), int(r["period"]), r["course_id"], r["teacher_id"], r["room_id"])
                for r in rows
            )
        finally:
            con.close()

    def _where(self, zone: ZoneDefinition):
        if zone.zone_type == "teacher":
            return "teacher_id = ?", (zone.entity_id,)
        if zone.zone_type == "course":
            return "course_id = ?", (zone.entity_id,)
        if zone.zone_type == "room":
            return "room_id = ?", (zone.entity_id,)
        if zone.zone_type == "time":
            return "day = ? AND period BETWEEN ? AND ?", (zone.day, zone.start_period, zone.end_period)
        raise ValueError(f"Zona no soportada: {zone.zone_type}")
