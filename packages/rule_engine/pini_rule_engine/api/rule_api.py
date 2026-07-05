from pini_rule_engine.services.rule_service import RuleService

class RuleApi:
    def __init__(self, service: RuleService):
        self.service = service

    def is_enabled(self, code: str) -> bool:
        return self.service.is_enabled(code)

    def get_parameter(self, rule_code: str, key: str, default: str | None = None) -> str | None:
        return self.service.get_parameter(rule_code, key, default)

    def get_max_consecutive(self, subject: str, course_level: int) -> int | None:
        return self.service.get_max_consecutive(subject, course_level)

    def contexts_must_be_after_break(self) -> bool:
        return self.service.contexts_must_be_after_break()
