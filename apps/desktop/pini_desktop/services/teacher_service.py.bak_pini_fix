import sqlite3
from dataclasses import dataclass
from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database

@dataclass(frozen=True)
class Teacher:
    id: int | None
    code: str
    name: str
    surname: str
    speciality: str
    weekly_hours: int = 25
    max_daily_sessions: int = 5

    @property
    def full_name(self) -> str:
        return f"{self.name} {self.surname}".strip()

class TeacherService:
    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        initialise_database()

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def list_teachers(self) -> list[Teacher]:
        connection = self._connect()
        try:
            rows = connection.execute(
                "SELECT id, code, name, surname, speciality, weekly_hours, max_daily_sessions FROM teachers ORDER BY surname, name"
            ).fetchall()
            return [self._row_to_teacher(row) for row in rows]
        finally:
            connection.close()

    def create_teacher(self, teacher: Teacher) -> int:
        connection = self._connect()
        try:
            cursor = connection.execute(
                "INSERT INTO teachers(code, name, surname, speciality, weekly_hours, max_daily_sessions) VALUES (?, ?, ?, ?, ?, ?)",
                (teacher.code.strip(), teacher.name.strip(), teacher.surname.strip(), teacher.speciality.strip(), int(teacher.weekly_hours), int(teacher.max_daily_sessions)),
            )
            connection.commit()
            return int(cursor.lastrowid)
        finally:
            connection.close()

    def update_teacher(self, teacher: Teacher) -> None:
        if teacher.id is None:
            raise ValueError("No se puede actualizar un profesor sin id.")
        connection = self._connect()
        try:
            connection.execute(
                "UPDATE teachers SET code=?, name=?, surname=?, speciality=?, weekly_hours=?, max_daily_sessions=? WHERE id=?",
                (teacher.code.strip(), teacher.name.strip(), teacher.surname.strip(), teacher.speciality.strip(), int(teacher.weekly_hours), int(teacher.max_daily_sessions), teacher.id),
            )
            connection.commit()
        finally:
            connection.close()

    def delete_teacher(self, teacher_id: int) -> None:
        connection = self._connect()
        try:
            connection.execute("DELETE FROM teachers WHERE id=?", (teacher_id,))
            connection.commit()
        finally:
            connection.close()

    def _row_to_teacher(self, row) -> Teacher:
        return Teacher(
            id=int(row["id"]),
            code=row["code"],
            name=row["name"],
            surname=row["surname"],
            speciality=row["speciality"],
            weekly_hours=int(row["weekly_hours"]),
            max_daily_sessions=int(row["max_daily_sessions"]),
        )
