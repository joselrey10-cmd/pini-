import sqlite3
from dataclasses import dataclass

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database


@dataclass(frozen=True)
class CourseSubject:
    id: int | None
    course_id: int
    subject_id: int
    weekly_sessions: int
    preferred_teacher_id: int | None = None
    required_room_type: str = ""
    notes: str = ""

    course_code: str = ""
    subject_name: str = ""
    teacher_name: str = ""


class CourseSubjectService:
    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        initialise_database()

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def list_assignments(self) -> list[CourseSubject]:
        connection = self._connect()
        try:
            rows = connection.execute(
                '''
                SELECT cs.id, cs.course_id, cs.subject_id, cs.weekly_sessions,
                       cs.preferred_teacher_id, cs.required_room_type, cs.notes,
                       c.code AS course_code,
                       s.name AS subject_name,
                       COALESCE(t.name || ' ' || t.surname, '') AS teacher_name
                FROM course_subjects cs
                JOIN courses c ON c.id = cs.course_id
                JOIN subjects s ON s.id = cs.subject_id
                LEFT JOIN teachers t ON t.id = cs.preferred_teacher_id
                ORDER BY c.level, c.group_name, s.name
                '''
            ).fetchall()
            return [self._row_to_assignment(row) for row in rows]
        finally:
            connection.close()

    def create_assignment(self, assignment: CourseSubject) -> int:
        connection = self._connect()
        try:
            cursor = connection.execute(
                '''
                INSERT INTO course_subjects(
                    course_id, subject_id, weekly_sessions,
                    preferred_teacher_id, required_room_type, notes
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ''',
                (
                    assignment.course_id,
                    assignment.subject_id,
                    int(assignment.weekly_sessions),
                    assignment.preferred_teacher_id,
                    assignment.required_room_type.strip(),
                    assignment.notes.strip(),
                ),
            )
            connection.commit()
            return int(cursor.lastrowid)
        finally:
            connection.close()

    def update_assignment(self, assignment: CourseSubject) -> None:
        if assignment.id is None:
            raise ValueError("No se puede actualizar una asignación sin id.")
        connection = self._connect()
        try:
            connection.execute(
                '''
                UPDATE course_subjects
                SET course_id=?, subject_id=?, weekly_sessions=?,
                    preferred_teacher_id=?, required_room_type=?, notes=?
                WHERE id=?
                ''',
                (
                    assignment.course_id,
                    assignment.subject_id,
                    int(assignment.weekly_sessions),
                    assignment.preferred_teacher_id,
                    assignment.required_room_type.strip(),
                    assignment.notes.strip(),
                    assignment.id,
                ),
            )
            connection.commit()
        finally:
            connection.close()

    def delete_assignment(self, assignment_id: int) -> None:
        connection = self._connect()
        try:
            connection.execute("DELETE FROM course_subjects WHERE id=?", (assignment_id,))
            connection.commit()
        finally:
            connection.close()

    def _row_to_assignment(self, row) -> CourseSubject:
        return CourseSubject(
            id=int(row["id"]),
            course_id=int(row["course_id"]),
            subject_id=int(row["subject_id"]),
            weekly_sessions=int(row["weekly_sessions"]),
            preferred_teacher_id=row["preferred_teacher_id"],
            required_room_type=row["required_room_type"] or "",
            notes=row["notes"] or "",
            course_code=row["course_code"],
            subject_name=row["subject_name"],
            teacher_name=row["teacher_name"] or "",
        )
