from pini_rule_engine.services.rule_service import RuleService

class RuleValidator:
    def validate_all(self, service: RuleService) -> list[str]:
        errors: list[str] = []
        raw_general = service.get_parameter("C006", "general_max_consecutive", "1")
        try:
            general = int(raw_general or "1")
            if general < 1:
                errors.append("C006: el máximo general debe ser al menos 1.")
        except ValueError:
            errors.append("C006: el máximo general debe ser numérico.")
        return errors
