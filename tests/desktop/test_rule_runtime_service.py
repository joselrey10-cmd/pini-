from pathlib import Path

from pini_desktop.services.dynamic_rule_service import DynamicRule, DynamicRuleService
from pini_desktop.services.rule_runtime_service import RuleRuntimeService


def test_dynamic_rule_forbids_period(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    rule_service = DynamicRuleService(database_path=db)
    rule_service.create_rule(
        DynamicRule(None, "R100", "EF no última hora", "Materia", "No permitir franja", "Obligatoria", "Educación Física", 1, 6, "", True, "")
    )

    runtime = RuleRuntimeService(database_path=db)

    decision = runtime.is_period_allowed(
        course_code="1A",
        subject_name="Educación Física",
        teacher_name="Ana",
        room_type="Gimnasio",
        day=1,
        period=6,
        is_after_break=True,
    )

    assert decision.allowed is False


def test_after_break_rule_blocks_before_break(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    rule_service = DynamicRuleService(database_path=db)
    rule_service.create_rule(
        DynamicRule(None, "R101", "Contextos después del recreo", "Materia", "Después del recreo", "Obligatoria", "Contextos", None, None, "Sí", True, "")
    )

    runtime = RuleRuntimeService(database_path=db)

    decision = runtime.is_period_allowed(
        course_code="1A",
        subject_name="Contextos",
        teacher_name="Ana",
        room_type="Ordinaria",
        day=1,
        period=2,
        is_after_break=False,
    )

    assert decision.allowed is False
