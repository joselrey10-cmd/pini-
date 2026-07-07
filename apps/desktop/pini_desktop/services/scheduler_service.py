import sqlite3
from dataclasses import dataclass

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database
from pini_desktop.services.project_validation_service import ProjectValidationService, ValidationSeverity
from pini_desktop.services.rule_runtime_service import RuleRuntimeService
from pini_desktop.services.scheduler.basic_engine import BasicSchedulerEngine
from pini_desktop.services.scheduler.ortools_engine import OrToolsSchedulerEngine
from pini_desktop.services.scheduler.repository import SchedulerRepository


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
        initialise_database(database_path=self.database_path)

        self.repository = SchedulerRepository(database_path)
        self.rule_runtime = RuleRuntimeService(database_path)

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def clear_generated_schedule(self) -> None:
        self.repository.clear_generated_schedule()

    def generate_basic_schedule(self) -> list[str]:
        return self._generate("basic")

    def generate_ortools_schedule(self) -> list[str]:
        return self._generate("ortools")

    def _generate(self, engine_name: str) -> list[str]:
        validator = ProjectValidationService(database_path=self.database_path)
        blocking = [i for i in validator.validate() if i.severity == ValidationSeverity.ERROR]
        if blocking:
            return [f"{i.code}: {i.message}" for i in blocking]

        self.repository.clear_generated_schedule()
        engine = (
            OrToolsSchedulerEngine(self.repository, self.rule_runtime)
            if engine_name == "ortools"
            else BasicSchedulerEngine(self.repository, self.rule_runtime)
        )
        result = engine.generate()
        self.repository.save_placements(result.placements)
        return result.warnings

    def list_sessions(self) -> list[ScheduleSession]:
        connection = self._connect()
        try:
            rows = connection.execute(
                """
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
                """
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
