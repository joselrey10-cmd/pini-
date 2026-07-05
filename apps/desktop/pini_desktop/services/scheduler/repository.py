import sqlite3

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database
from pini_desktop.services.scheduler.domain import ScheduleAssignment, SchedulePeriod, SchedulePlacement


class SchedulerRepository:
    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        initialise_database()

    def connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def list_periods(self) -> list[SchedulePeriod]:
        con = self.connect()
        try:
            rows = con.execute(
                "SELECT day, period, is_after_break FROM timetable_periods ORDER BY day, period"
            ).fetchall()
            return [
                SchedulePeriod(
                    day=int(row["day"]),
                    period=int(row["period"]),
                    is_after_break=bool(row["is_after_break"]),
                )
                for row in rows
            ]
        finally:
            con.close()

    def list_assignments(self) -> list[ScheduleAssignment]:
        con = self.connect()
        try:
            rows = con.execute(
                """
                SELECT cs.course_id, cs.subject_id, cs.weekly_sessions,
                       cs.preferred_teacher_id, cs.required_room_type,
                       c.code AS course_code,
                       s.name AS subject_name
                FROM course_subjects cs
                JOIN courses c ON c.id = cs.course_id
                JOIN subjects s ON s.id = cs.subject_id
                ORDER BY c.level, c.group_name, s.name
                """
            ).fetchall()
            return [
                ScheduleAssignment(
                    course_id=int(row["course_id"]),
                    subject_id=int(row["subject_id"]),
                    weekly_sessions=int(row["weekly_sessions"]),
                    preferred_teacher_id=row["preferred_teacher_id"],
                    required_room_type=row["required_room_type"] or "",
                    course_code=row["course_code"],
                    subject_name=row["subject_name"],
                )
                for row in rows
            ]
        finally:
            con.close()

    def teacher_name(self, teacher_id) -> str:
        if teacher_id is None:
            return ""
        con = self.connect()
        try:
            row = con.execute("SELECT name, surname FROM teachers WHERE id=?", (teacher_id,)).fetchone()
            return f"{row['name']} {row['surname']}" if row else ""
        finally:
            con.close()

    def find_room(self, required_room_type: str | None):
        con = self.connect()
        try:
            if not required_room_type:
                row = con.execute("SELECT id FROM rooms WHERE available=1 ORDER BY id LIMIT 1").fetchone()
            else:
                row = con.execute(
                    "SELECT id FROM rooms WHERE available=1 AND room_type=? ORDER BY id LIMIT 1",
                    (required_room_type,),
                ).fetchone()
            return row["id"] if row else None
        finally:
            con.close()

    def teacher_forbidden(self, teacher_id: int, day: int, period: int) -> bool:
        con = self.connect()
        try:
            row = con.execute(
                "SELECT status FROM teacher_availability WHERE teacher_id=? AND day=? AND period=?",
                (teacher_id, day, period),
            ).fetchone()
            return bool(row and row["status"] == "FORBIDDEN")
        finally:
            con.close()

    def clear_generated_schedule(self) -> None:
        con = self.connect()
        try:
            con.execute("DELETE FROM schedule_sessions WHERE locked = 0")
            con.commit()
        finally:
            con.close()

    def save_placements(self, placements: list[SchedulePlacement]) -> None:
        con = self.connect()
        try:
            for placement in placements:
                con.execute(
                    """
                    INSERT INTO schedule_sessions(course_id, subject_id, teacher_id, room_id, day, period, locked, generated_by)
                    VALUES (?, ?, ?, ?, ?, ?, 0, ?)
                    """,
                    (
                        placement.course_id,
                        placement.subject_id,
                        placement.teacher_id,
                        placement.room_id,
                        placement.day,
                        placement.period,
                        placement.generated_by,
                    ),
                )
            con.commit()
        finally:
            con.close()
