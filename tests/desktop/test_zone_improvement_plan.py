from pini_desktop.services.editor.optimization.iterative_zone_search import IterativeZoneSearchResult, IterativeZoneStep
from pini_desktop.services.editor.optimization.zone_definition import ZoneDefinition
from pini_desktop.services.editor.optimization.zone_improvement_plan import ZoneImprovementPlanner
from pini_desktop.services.editor.optimization.zone_optimizer import ZoneOptimizationSuggestion


def test_zone_improvement_planner_builds_plan():
    zone = ZoneDefinition("teacher", entity_id=1)
    result = IterativeZoneSearchResult(
        zone=zone,
        iterations=1,
        accumulated_delta=1.5,
        steps=(
            IterativeZoneStep(
                iteration=1,
                suggestion=ZoneOptimizationSuggestion(1, 2, 3, 1.5, "Mover"),
                accumulated_delta=1.5,
            ),
        ),
    )

    plan = ZoneImprovementPlanner().build_plan(result)

    assert plan.has_actions
    assert plan.estimated_delta == 1.5
    assert plan.actions[0].session_id == 1


def test_zone_plan_report():
    from pini_desktop.services.editor.optimization.zone_plan_report import ZoneImprovementPlanReport

    zone = ZoneDefinition("teacher", entity_id=1)
    result = IterativeZoneSearchResult(zone, 0, (), 0)
    plan = ZoneImprovementPlanner().build_plan(result)
    report = ZoneImprovementPlanReport().build(plan)

    assert report["zone"]


def test_zone_plan_preview_dialog_import():
    from pini_desktop.ui.views.zone_plan_preview_dialog import ZonePlanPreviewDialog

    assert ZonePlanPreviewDialog is not None
