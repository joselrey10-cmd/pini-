import sqlite3
from dataclasses import dataclass

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database


@dataclass(frozen=True)
class ScheduleCell:
    id: int | None
    day: int
    period: int
    course_code: str
    subject_name: str
    teacher_name: str
    room_name: str


class ScheduleViewService:
    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        initialise_database(database_path=self.database_path)

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def list_courses(self) -> list[tuple[int, str]]:
        connection = self._connect()
        try:
            rows = connection.execute("SELECT id, code FROM courses ORDER BY level, group_name").fetchall()
            return [(int(row["id"]), row["code"]) for row in rows]
        finally:
            connection.close()

    def list_teachers(self) -> list[tuple[int, str]]:
        connection = self._connect()
        try:
            rows = connection.execute(
                "SELECT id, code, name, surname FROM teachers ORDER BY surname, name"
            ).fetchall()
            return [(int(row["id"]), f"{row['code']} - {row['name']} {row['surname']}") for row in rows]
        finally:
            connection.close()

    def course_matrix(self, course_id: int) -> dict[tuple[int, int], ScheduleCell]:
        return self._matrix("ss.course_id = ?", course_id)

    def teacher_matrix(self, teacher_id: int) -> dict[tuple[int, int], ScheduleCell]:
        return self._matrix("ss.teacher_id = ?", teacher_id)

    def _matrix(self, where_clause: str, entity_id: int) -> dict[tuple[int, int], ScheduleCell]:
        connection = self._connect()
        try:
            rows = connection.execute(
                f"""
                SELECT ss.id, ss.day, ss.period,
                       c.code AS course_code,
                       s.name AS subject_name,
                       COALESCE(t.name || ' ' || t.surname, '') AS teacher_name,
                       COALESCE(r.name, '') AS room_name
                FROM schedule_sessions ss
                JOIN courses c ON c.id = ss.course_id
                JOIN subjects s ON s.id = ss.subject_id
                LEFT JOIN teachers t ON t.id = ss.teacher_id
                LEFT JOIN rooms r ON r.id = ss.room_id
                WHERE {where_clause}
                ORDER BY ss.day, ss.period
                """,
                (entity_id,),
            ).fetchall()

            return {
                (int(row["day"]), int(row["period"])): ScheduleCell(
                    id=int(row["id"]),
                    day=int(row["day"]),
                    period=int(row["period"]),
                    course_code=row["course_code"],
                    subject_name=row["subject_name"],
                    teacher_name=row["teacher_name"] or "",
                    room_name=row["room_name"] or "",
                )
                for row in rows
            }
        finally:
            connection.close()
