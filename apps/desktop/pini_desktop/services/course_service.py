import sqlite3
from dataclasses import dataclass

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database


@dataclass(frozen=True)
class Course:
    id: int | None
    code: str
    stage: str
    level: int
    group_name: str
    students: int = 25
    tutor_teacher_id: int | None = None

    @property
    def display_name(self) -> str:
        return f"{self.level}º{self.group_name}" if self.stage.lower() == "primaria" else f"{self.stage} {self.level}{self.group_name}"


class CourseService:
    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        initialise_database()

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def list_courses(self) -> list[Course]:
        connection = self._connect()
        try:
            rows = connection.execute(
                '''
                SELECT id, code, stage, level, group_name, students, tutor_teacher_id
                FROM courses
                ORDER BY stage, level, group_name
                '''
            ).fetchall()
            return [self._row_to_course(row) for row in rows]
        finally:
            connection.close()

    def create_course(self, course: Course) -> int:
        connection = self._connect()
        try:
            cursor = connection.execute(
                '''
                INSERT INTO courses(code, stage, level, group_name, students, tutor_teacher_id)
                VALUES (?, ?, ?, ?, ?, ?)
                ''',
                (
                    course.code.strip(),
                    course.stage.strip(),
                    int(course.level),
                    course.group_name.strip().upper(),
                    int(course.students),
                    course.tutor_teacher_id,
                ),
            )
            connection.commit()
            return int(cursor.lastrowid)
        finally:
            connection.close()

    def update_course(self, course: Course) -> None:
        if course.id is None:
            raise ValueError("No se puede actualizar un curso sin id.")

        connection = self._connect()
        try:
            connection.execute(
                '''
                UPDATE courses
                SET code=?, stage=?, level=?, group_name=?, students=?, tutor_teacher_id=?
                WHERE id=?
                ''',
                (
                    course.code.strip(),
                    course.stage.strip(),
                    int(course.level),
                    course.group_name.strip().upper(),
                    int(course.students),
                    course.tutor_teacher_id,
                    course.id,
                ),
            )
            connection.commit()
        finally:
            connection.close()

    def delete_course(self, course_id: int) -> None:
        connection = self._connect()
        try:
            connection.execute("DELETE FROM courses WHERE id=?", (course_id,))
            connection.commit()
        finally:
            connection.close()

    def _row_to_course(self, row) -> Course:
        return Course(
            id=int(row["id"]),
            code=row["code"],
            stage=row["stage"],
            level=int(row["level"]),
            group_name=row["group_name"],
            students=int(row["students"]),
            tutor_teacher_id=row["tutor_teacher_id"],
        )
