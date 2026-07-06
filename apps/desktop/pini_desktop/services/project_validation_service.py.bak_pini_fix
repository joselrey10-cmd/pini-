import sqlite3
from dataclasses import dataclass
from enum import Enum

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database


class ValidationSeverity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass(frozen=True)
class ValidationIssue:
    severity: ValidationSeverity
    code: str
    message: str
    area: str


class ProjectValidationService:
    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        initialise_database()

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def validate(self) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        connection = self._connect()
        try:
            counts = {
                "teachers": self._count(connection, "teachers"),
                "courses": self._count(connection, "courses"),
                "subjects": self._count(connection, "subjects"),
                "rooms": self._count(connection, "rooms"),
                "course_subjects": self._count(connection, "course_subjects"),
                "timetable_periods": self._count(connection, "timetable_periods"),
            }

            if counts["teachers"] == 0:
                issues.append(ValidationIssue(ValidationSeverity.ERROR, "VAL001", "No hay profesorado creado.", "Profesorado"))

            if counts["courses"] == 0:
                issues.append(ValidationIssue(ValidationSeverity.ERROR, "VAL002", "No hay cursos creados.", "Cursos"))

            if counts["subjects"] == 0:
                issues.append(ValidationIssue(ValidationSeverity.ERROR, "VAL003", "No hay materias creadas.", "Materias"))

            if counts["rooms"] == 0:
                issues.append(ValidationIssue(ValidationSeverity.WARNING, "VAL004", "No hay aulas creadas.", "Aulas"))

            if counts["course_subjects"] == 0:
                issues.append(ValidationIssue(ValidationSeverity.ERROR, "VAL005", "No hay materias asignadas a cursos.", "Materias por curso"))

            if counts["timetable_periods"] == 0:
                issues.append(ValidationIssue(ValidationSeverity.ERROR, "VAL006", "No se han generado los periodos del horario general.", "Horario general"))

            issues.extend(self._validate_teacher_hours(connection))
            issues.extend(self._validate_course_subjects_without_teacher(connection))
            issues.extend(self._validate_subject_consecutive_rules(connection))

            if not issues:
                issues.append(ValidationIssue(ValidationSeverity.INFO, "VAL000", "El proyecto está preparado para iniciar el motor de horarios.", "Proyecto"))

            return issues
        finally:
            connection.close()

    def has_blocking_errors(self) -> bool:
        return any(issue.severity == ValidationSeverity.ERROR for issue in self.validate())

    def _count(self, connection, table: str) -> int:
        row = connection.execute(f"SELECT COUNT(*) AS total FROM {table}").fetchone()
        return int(row["total"])

    def _validate_teacher_hours(self, connection) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        rows = connection.execute(
            '''
            SELECT id, code, name, surname, weekly_hours, max_daily_sessions
            FROM teachers
            '''
        ).fetchall()

        for row in rows:
            max_possible = int(row["max_daily_sessions"]) * 5
            if int(row["weekly_hours"]) > max_possible:
                issues.append(
                    ValidationIssue(
                        ValidationSeverity.ERROR,
                        "VAL101",
                        f"{row['name']} {row['surname']} tiene {row['weekly_hours']} horas, pero su máximo diario solo permite {max_possible}.",
                        "Profesorado",
                    )
                )
        return issues

    def _validate_course_subjects_without_teacher(self, connection) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        rows = connection.execute(
            '''
            SELECT c.code AS course_code, s.name AS subject_name
            FROM course_subjects cs
            JOIN courses c ON c.id = cs.course_id
            JOIN subjects s ON s.id = cs.subject_id
            WHERE cs.preferred_teacher_id IS NULL
            ORDER BY c.code, s.name
            '''
        ).fetchall()

        for row in rows:
            issues.append(
                ValidationIssue(
                    ValidationSeverity.WARNING,
                    "VAL201",
                    f"{row['course_code']} - {row['subject_name']} no tiene profesor preferente asignado.",
                    "Materias por curso",
                )
            )
        return issues

    def _validate_subject_consecutive_rules(self, connection) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        rows = connection.execute(
            '''
            SELECT code, name, max_consecutive, allows_double_session
            FROM subjects
            WHERE max_consecutive > 1 AND allows_double_session = 0
            '''
        ).fetchall()

        for row in rows:
            issues.append(
                ValidationIssue(
                    ValidationSeverity.WARNING,
                    "VAL301",
                    f"{row['name']} permite {row['max_consecutive']} consecutivas pero no tiene marcada la doble sesión.",
                    "Materias",
                )
            )
        return issues
