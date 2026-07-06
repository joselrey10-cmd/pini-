from dataclasses import dataclass
import sqlite3
from pathlib import Path

from .models import Absence, CandidateTeacher


@dataclass(frozen=True)
class ScheduledSessionInfo:
    teacher: str
    course: str
    subject: str
    room: str
    day: int
    period: int
    required_speciality: str = ""


class PiniSubstitutionDataAdapter:
    """Adaptador entre la base SQLite de Pini y el motor de sustituciones."""

    def __init__(self, database_path):
        self.database_path = Path(database_path)

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def absence_from_teacher_period(self, teacher_id: int, day: int, period: int) -> Absence:
        con = self._connect()
        try:
            row = con.execute(
                """
                SELECT
                    t.name || ' ' || t.surname AS teacher_name,
                    c.code AS course_code,
                    s.name AS subject_name,
                    COALESCE(r.name, '') AS room_name,
                    COALESCE(s.required_speciality, '') AS required_speciality
                FROM schedule_sessions ss
                JOIN teachers t ON t.id = ss.teacher_id
                JOIN courses c ON c.id = ss.course_id
                JOIN subjects s ON s.id = ss.subject_id
                LEFT JOIN rooms r ON r.id = ss.room_id
                WHERE ss.teacher_id=? AND ss.day=? AND ss.period=?
                LIMIT 1
                """,
                (teacher_id, day, period),
            ).fetchone()

            if not row:
                teacher = con.execute(
                    "SELECT name || ' ' || surname AS teacher_name FROM teachers WHERE id=?",
                    (teacher_id,),
                ).fetchone()
                teacher_name = teacher["teacher_name"] if teacher else str(teacher_id)
                return Absence(teacher=teacher_name, day=day, period=period)

            return Absence(
                teacher=row["teacher_name"],
                day=day,
                period=period,
                course=row["course_code"],
                subject=row["subject_name"],
                room=row["room_name"],
                required_speciality=row["required_speciality"] or "",
            )
        finally:
            con.close()

    def candidate_teachers(self, absent_teacher_id: int, day: int, period: int) -> list[CandidateTeacher]:
        con = self._connect()
        try:
            teachers = con.execute(
                """
                SELECT id, name, surname, speciality
                FROM teachers
                WHERE id != ?
                ORDER BY surname, name
                """,
                (absent_teacher_id,),
            ).fetchall()

            candidates = []
            for teacher in teachers:
                teacher_id = int(teacher["id"])
                busy = self._is_teacher_busy(con, teacher_id, day, period)
                forbidden = self._is_forbidden(con, teacher_id, day, period)
                status = self._availability_status(con, teacher_id, day, period)

                if forbidden:
                    continue

                candidates.append(
                    CandidateTeacher(
                        name=f"{teacher['name']} {teacher['surname']}",
                        speciality=teacher["speciality"] or "",
                        is_free=not busy,
                        is_on_duty=status == "PREFERRED",
                        same_building=True,
                        can_move_support=busy and status == "AVOID",
                        breaks_important_support=False,
                        current_task="Ocupado" if busy else "",
                    )
                )

            return candidates
        finally:
            con.close()

    def _is_teacher_busy(self, con, teacher_id: int, day: int, period: int) -> bool:
        row = con.execute(
            "SELECT id FROM schedule_sessions WHERE teacher_id=? AND day=? AND period=? LIMIT 1",
            (teacher_id, day, period),
        ).fetchone()
        return row is not None

    def _availability_status(self, con, teacher_id: int, day: int, period: int) -> str:
        row = con.execute(
            "SELECT status FROM teacher_availability WHERE teacher_id=? AND day=? AND period=?",
            (teacher_id, day, period),
        ).fetchone()
        return row["status"] if row else "AVAILABLE"

    def _is_forbidden(self, con, teacher_id: int, day: int, period: int) -> bool:
        return self._availability_status(con, teacher_id, day, period) == "FORBIDDEN"
