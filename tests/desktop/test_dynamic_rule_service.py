from pathlib import Path
from pini_desktop.services.dynamic_rule_service import DynamicRule, DynamicRuleService

def test_dynamic_rule_crud(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    service = DynamicRuleService(database_path=db)
    rule_id = service.create_rule(DynamicRule(None, "R100", "EF no última hora", "Materia", "No permitir franja", "Obligatoria", "Educación Física", 5, 6, "", True, "Prueba"))
    assert service.list_rules()[0].id == rule_id
    service.update_rule(DynamicRule(rule_id, "R100", "EF evitar última hora", "Materia", "Evitar franja", "Preferente", "Educación Física", 5, 6, "", True, "Ajustado"))
    assert service.list_rules()[0].priority == "Preferente"
    service.delete_rule(rule_id)
    assert service.list_rules() == []

def test_seed_center_rules(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    service = DynamicRuleService(database_path=db)
    service.seed_center_rules()
    codes = {r.code for r in service.list_rules()}
    assert {"R001", "R002", "R003"} <= codes
