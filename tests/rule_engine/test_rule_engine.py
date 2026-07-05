from pini_rule_engine.api.rule_api import RuleApi
from pini_rule_engine.services.rule_service import RuleService
from pini_rule_engine.services.validator import RuleValidator

def test_default_rule_engine_configuration():
    service = RuleService.create_in_memory()
    service.seed_default_rules()
    api = RuleApi(service)

    assert api.is_enabled("P001") is True
    assert api.get_parameter("C006", "general_max_consecutive") == "1"
    assert api.get_max_consecutive("Lengua", 3) == 1
    assert api.get_max_consecutive("Inglés", 4) == 2
    assert api.get_max_consecutive("Inglés", 5) == 2
    assert api.get_max_consecutive("Inglés", 6) == 2
    assert api.contexts_must_be_after_break() is True

def test_rule_validator_accepts_default_configuration():
    service = RuleService.create_in_memory()
    service.seed_default_rules()
    errors = RuleValidator().validate_all(service)
    assert errors == []
