import sqlite3
from dataclasses import dataclass

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database
from pini_desktop.services.project_validation_service import ProjectValidationService, ValidationSeverity


@dataclass(frozen=True)
class ScheduleSession:
    id: int | None
    course_id: int
    subject_id: int
    teacher_id: int | None
    room_id: int | None
    day: int
    period: int
    course_code: str = ""
    subject_name: str = ""
    teacher_name: str = ""
    room_name: str = ""


class SchedulerService:
    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        initialise_database()

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def clear_generated_schedule(self) -> None:
        connection = self._connect()
        try:
            connection.execute("DELETE FROM schedule_sessions WHERE locked = 0")
            connection.commit()
        finally:
            connection.close()

    def generate_basic_schedule(self) -> list[str]:
        validator = ProjectValidationService(database_path=self.database_path)
        issues = validator.validate()
        blocking = [issue for issue in issues if issue.severity == ValidationSeverity.ERROR]
        if blocking:
            return [f"{issue.code}: {issue.message}" for issue in blocking]

        self.clear_generated_schedule()
        warnings: list[str] = []

        connection = self._connect()
        try:
            periods = connection.execute(
                "SELECT day, period FROM timetable_periods ORDER BY day, period"
            ).fetchall()

            assignments = connection.execute(
                '''
                SELECT cs.course_id, cs.subject_id, cs.weekly_sessions,
                       cs.preferred_teacher_id, cs.required_room_type,
                       c.code AS course_code, s.name AS subject_name
                FROM course_subjects cs
                JOIN courses c ON c.id = cs.course_id
                JOIN subjects s ON s.id = cs.subject_id
                ORDER BY c.level, c.group_name, s.name
                '''
            ).fetchall()

            if not periods:
                return ["No hay periodos generados. Ve a Centro > Horario general y genera los periodos."]

            occupied_course: set[tuple[int, int, int]] = set()
            occupied_teacher: set[tuple[int, int, int]] = set()
            occupied_room: set[tuple[int, int, int]] = set()

            for assignment in assignments:
                sessions_needed = int(assignment["weekly_sessions"])
                placed = 0

                for period_row in periods:
                    if placed >= sessions_needed:
                        break

                    day = int(period_row["day"])
                    period = int(period_row["period"])
                    course_id = int(assignment["course_id"])
                    teacher_id = assignment["preferred_teacher_id"]
                    room_id = self._find_room(connection, assignment["required_room_type"])

                    if (course_id, day, period) in occupied_course:
                        continue

                    if teacher_id is not None and (int(teacher_id), day, period) in occupied_teacher:
                        continue

                    if room_id is not None and (int(room_id), day, period) in occupied_room:
                        continue

                    if teacher_id is not None and self._teacher_forbidden(connection, int(teacher_id), day, period):
                        continue

                    connection.execute(
                        '''
                        INSERT INTO schedule_sessions(course_id, subject_id, teacher_id, room_id, day, period, locked, generated_by)
                        VALUES (?, ?, ?, ?, ?, ?, 0, 'basic')
                        ''',
                        (
                            course_id,
                            int(assignment["subject_id"]),
                            int(teacher_id) if teacher_id is not None else None,
                            int(room_id) if room_id is not None else None,
                            day,
                            period,
                        ),
                    )

                    occupied_course.add((course_id, day, period))
                    if teacher_id is not None:
                        occupied_teacher.add((int(teacher_id), day, period))
                    if room_id is not None:
                        occupied_room.add((int(room_id), day, period))

                    placed += 1

                if placed < sessions_needed:
                    warnings.append(
                        f"No se pudieron colocar todas las sesiones de {assignment['subject_name']} en {assignment['course_code']} ({placed}/{sessions_needed})."
                    )

            connection.commit()
            return warnings
        finally:
            connection.close()

    def list_sessions(self) -> list[ScheduleSession]:
        connection = self._connect()
        try:
            rows = connection.execute(
                '''
                SELECT ss.id, ss.course_id, ss.subject_id, ss.teacher_id, ss.room_id,
                       ss.day, ss.period,
                       c.code AS course_code,
                       s.name AS subject_name,
                       COALESCE(t.name || ' ' || t.surname, '') AS teacher_name,
                       COALESCE(r.name, '') AS room_name
                FROM schedule_sessions ss
                JOIN courses c ON c.id = ss.course_id
                JOIN subjects s ON s.id = ss.subject_id
                LEFT JOIN teachers t ON t.id = ss.teacher_id
                LEFT JOIN rooms r ON r.id = ss.room_id
                ORDER BY ss.day, ss.period, c.code
                '''
            ).fetchall()
            return [
                ScheduleSession(
                    id=int(row["id"]),
                    course_id=int(row["course_id"]),
                    subject_id=int(row["subject_id"]),
                    teacher_id=row["teacher_id"],
                    room_id=row["room_id"],
                    day=int(row["day"]),
                    period=int(row["period"]),
                    course_code=row["course_code"],
                    subject_name=row["subject_name"],
                    teacher_name=row["teacher_name"] or "",
                    room_name=row["room_name"] or "",
                )
                for row in rows
            ]
        finally:
            connection.close()

    def _find_room(self, connection, required_room_type: str | None):
        if not required_room_type:
            row = connection.execute(
                "SELECT id FROM rooms WHERE available=1 ORDER BY id LIMIT 1"
            ).fetchone()
        else:
            row = connection.execute(
                "SELECT id FROM rooms WHERE available=1 AND room_type=? ORDER BY id LIMIT 1",
                (required_room_type,),
            ).fetchone()

        return row["id"] if row else None

    def _teacher_forbidden(self, connection, teacher_id: int, day: int, period: int) -> bool:
        row = connection.execute(
            '''
            SELECT status FROM teacher_availability
            WHERE teacher_id=? AND day=? AND period=?
            ''',
            (teacher_id, day, period),
        ).fetchone()
        return bool(row and row["status"] == "FORBIDDEN")
