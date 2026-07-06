import sqlite3
from dataclasses import dataclass

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database


@dataclass(frozen=True)
class Subject:
    id: int | None
    code: str
    name: str
    weekly_sessions: int = 1
    required_speciality: str = ""
    room_type: str = ""
    max_consecutive: int = 1
    allows_double_session: bool = False


class SubjectService:
    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        initialise_database()

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def list_subjects(self) -> list[Subject]:
        connection = self._connect()
        try:
            rows = connection.execute(
                '''
                SELECT id, code, name, weekly_sessions, required_speciality,
                       room_type, max_consecutive, allows_double_session
                FROM subjects
                ORDER BY name
                '''
            ).fetchall()
            return [self._row_to_subject(row) for row in rows]
        finally:
            connection.close()

    def create_subject(self, subject: Subject) -> int:
        connection = self._connect()
        try:
            cursor = connection.execute(
                '''
                INSERT INTO subjects(code, name, weekly_sessions, required_speciality,
                                     room_type, max_consecutive, allows_double_session)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    subject.code.strip().upper(),
                    subject.name.strip(),
                    int(subject.weekly_sessions),
                    subject.required_speciality.strip(),
                    subject.room_type.strip(),
                    int(subject.max_consecutive),
                    int(subject.allows_double_session),
                ),
            )
            connection.commit()
            return int(cursor.lastrowid)
        finally:
            connection.close()

    def update_subject(self, subject: Subject) -> None:
        if subject.id is None:
            raise ValueError("No se puede actualizar una materia sin id.")

        connection = self._connect()
        try:
            connection.execute(
                '''
                UPDATE subjects
                SET code=?, name=?, weekly_sessions=?, required_speciality=?,
                    room_type=?, max_consecutive=?, allows_double_session=?
                WHERE id=?
                ''',
                (
                    subject.code.strip().upper(),
                    subject.name.strip(),
                    int(subject.weekly_sessions),
                    subject.required_speciality.strip(),
                    subject.room_type.strip(),
                    int(subject.max_consecutive),
                    int(subject.allows_double_session),
                    subject.id,
                ),
            )
            connection.commit()
        finally:
            connection.close()

    def delete_subject(self, subject_id: int) -> None:
        connection = self._connect()
        try:
            connection.execute("DELETE FROM subjects WHERE id=?", (subject_id,))
            connection.commit()
        finally:
            connection.close()

    def seed_default_subjects(self) -> None:
        if self.list_subjects():
            return
        defaults = [
            Subject(None, "LEN", "Lengua", 5, "Primaria", "Ordinaria", 1, False),
            Subject(None, "MAT", "Matemáticas", 5, "Primaria", "Ordinaria", 1, False),
            Subject(None, "ING", "Inglés", 3, "Inglés", "Ordinaria", 2, True),
            Subject(None, "EF", "Educación Física", 2, "Educación Física", "Gimnasio", 1, False),
            Subject(None, "MUS", "Música", 1, "Música", "Música", 1, False),
            Subject(None, "REL", "Religión", 1, "Religión", "Ordinaria", 1, False),
            Subject(None, "AE", "Atención Educativa", 1, "Primaria", "Ordinaria", 1, False),
            Subject(None, "CON", "Contextos", 3, "Primaria", "Ordinaria", 1, False),
        ]
        for subject in defaults:
            self.create_subject(subject)

    def _row_to_subject(self, row) -> Subject:
        return Subject(
            id=int(row["id"]),
            code=row["code"],
            name=row["name"],
            weekly_sessions=int(row["weekly_sessions"]),
            required_speciality=row["required_speciality"] or "",
            room_type=row["room_type"] or "",
            max_consecutive=int(row["max_consecutive"]),
            allows_double_session=bool(row["allows_double_session"]),
        )
