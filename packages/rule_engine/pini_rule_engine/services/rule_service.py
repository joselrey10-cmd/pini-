from pathlib import Path
from pini_rule_engine.domain.exception import RuleException
from pini_rule_engine.domain.parameter import RuleParameter
from pini_rule_engine.domain.rule import Rule, RuleType
from pini_rule_engine.persistence.database import connect, initialize
from pini_rule_engine.persistence.rule_repository import RuleRepository

class RuleService:
    def __init__(self, repository: RuleRepository):
        self.repository = repository

    @classmethod
    def create_in_memory(cls) -> "RuleService":
        connection = connect(":memory:")
        initialize(connection)
        return cls(RuleRepository(connection))

    @classmethod
    def create_sqlite(cls, database_path: str | Path) -> "RuleService":
        connection = connect(database_path)
        initialize(connection)
        return cls(RuleRepository(connection))

    def seed_default_rules(self) -> None:
        self.repository.clear_all()
        self.repository.save_rule(Rule("P001", "Profesor único", "Profesorado", RuleType.HARD, True, 1000, "Un profesor no puede impartir dos sesiones simultáneas."))
        self.repository.save_rule(Rule("C006", "Máximo sesiones consecutivas por área", "Cursos", RuleType.HARD, True, 1000, "Máximo de sesiones consecutivas por área."))
        self.repository.save_rule(Rule("C006.1", "Contextos después del recreo", "Cursos", RuleType.HARD, True, 1000, "Los contextos deben situarse después del recreo."))
        self.repository.save_parameter(RuleParameter("C006", "general_max_consecutive", "1"))
        self.repository.save_exception(RuleException("C006", "Inglés", 4, 6, "max_consecutive", "2"))
        self.repository.save_parameter(RuleParameter("C006.1", "contexts_after_break", "true"))

    def is_enabled(self, code: str) -> bool:
        rule = self.repository.get_rule(code)
        return bool(rule and rule.enabled)

    def get_parameter(self, rule_code: str, key: str, default: str | None = None) -> str | None:
        return self.repository.get_parameter(rule_code, key, default)

    def get_max_consecutive(self, subject: str, course_level: int) -> int | None:
        if not self.is_enabled("C006"):
            return None
        for exception in self.repository.list_exceptions("C006"):
            if exception.parameter == "max_consecutive" and exception.applies_to(subject, course_level):
                return int(exception.value)
        return int(self.get_parameter("C006", "general_max_consecutive", "1"))

    def contexts_must_be_after_break(self) -> bool:
        value = self.get_parameter("C006.1", "contexts_after_break", "false")
        return self.is_enabled("C006.1") and str(value).casefold() == "true"
