from dataclasses import dataclass

from pini_desktop.services.dynamic_rule_service import DynamicRule, DynamicRuleService


@dataclass(frozen=True)
class RuntimeDecision:
    allowed: bool
    reason: str = ""


class RuleRuntimeService:
    """Interpreta las reglas dinámicas activas para el generador.

    Esta primera versión aplica reglas simples basadas en texto:
    - No permitir franja.
    - Evitar franja.
    - Después del recreo.
    - Aula obligatoria.
    """

    def __init__(self, database_path=None):
        self.rule_service = DynamicRuleService(database_path) if database_path else DynamicRuleService()

    def active_rules(self) -> list[DynamicRule]:
        return [rule for rule in self.rule_service.list_rules() if rule.active]

    def is_period_allowed(
        self,
        *,
        course_code: str,
        subject_name: str,
        teacher_name: str,
        room_type: str,
        day: int,
        period: int,
        is_after_break: bool,
    ) -> RuntimeDecision:
        for rule in self.active_rules():
            if not self._target_matches(rule, course_code, subject_name, teacher_name, room_type):
                continue

            if rule.rule_type == "No permitir franja":
                if self._day_matches(rule, day) and self._period_matches(rule, period):
                    return RuntimeDecision(False, f"{rule.code}: {rule.name}")

            if rule.rule_type == "Después del recreo":
                if not is_after_break:
                    return RuntimeDecision(False, f"{rule.code}: {rule.name}")

        return RuntimeDecision(True)

    def is_room_allowed(self, *, subject_name: str, room_type: str) -> RuntimeDecision:
        for rule in self.active_rules():
            if rule.rule_type != "Aula obligatoria":
                continue
            if not self._target_matches(rule, "", subject_name, "", room_type):
                continue
            if rule.value and rule.value.casefold() != room_type.casefold():
                return RuntimeDecision(False, f"{rule.code}: {rule.name}")
        return RuntimeDecision(True)

    def preferred_period_score(
        self,
        *,
        course_code: str,
        subject_name: str,
        teacher_name: str,
        room_type: str,
        day: int,
        period: int,
    ) -> int:
        score = 0
        for rule in self.active_rules():
            if not self._target_matches(rule, course_code, subject_name, teacher_name, room_type):
                continue
            if not self._day_matches(rule, day) or not self._period_matches(rule, period):
                continue
            if rule.rule_type == "Preferir franja":
                score += 10
            elif rule.rule_type == "Evitar franja":
                score -= 10
        return score

    def _target_matches(
        self,
        rule: DynamicRule,
        course_code: str,
        subject_name: str,
        teacher_name: str,
        room_type: str,
    ) -> bool:
        target = (rule.target or "").strip()
        if not target or target.casefold() in {"todas", "todos", "cualquiera"}:
            return True

        candidates = [course_code, subject_name, teacher_name, room_type]
        target_cf = target.casefold()
        return any(target_cf in (candidate or "").casefold() for candidate in candidates)

    def _day_matches(self, rule: DynamicRule, day: int) -> bool:
        return rule.day is None or int(rule.day) == int(day)

    def _period_matches(self, rule: DynamicRule, period: int) -> bool:
        return rule.period is None or int(rule.period) == int(period)
