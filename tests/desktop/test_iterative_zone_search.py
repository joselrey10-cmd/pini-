from pini_desktop.services.editor.optimization.iterative_zone_report import IterativeZoneSearchReport
from pini_desktop.services.editor.optimization.iterative_zone_search import IterativeZoneSearch
from pini_desktop.services.editor.optimization.zone_definition import ZoneDefinition
from pini_desktop.services.editor.optimization.zone_optimizer import ZoneOptimizationResult, ZoneOptimizationSuggestion
from pini_desktop.services.editor.optimization.zone_score import ZoneScore


class FakeOptimizer:
    def optimize(self, zone, limit=5):
        return ZoneOptimizationResult(
            zone=zone,
            before=ZoneScore(sessions=2, gaps=1, last_periods=0, score=90),
            suggestions=(
                ZoneOptimizationSuggestion(1, 1, 2, 1.5, "Mover 1"),
                ZoneOptimizationSuggestion(2, 2, 3, 1.0, "Mover 2"),
            ),
        )


def test_iterative_zone_search_accumulates_steps():
    zone = ZoneDefinition("teacher", entity_id=1)
    result = IterativeZoneSearch(zone_optimizer=FakeOptimizer()).search(zone, max_iterations=2)

    assert result.has_improvement
    assert result.iterations == 2
    assert result.accumulated_delta == 2.5


def test_iterative_zone_report():
    zone = ZoneDefinition("teacher", entity_id=1)
    result = IterativeZoneSearch(zone_optimizer=FakeOptimizer()).search(zone, max_iterations=1)
    report = IterativeZoneSearchReport().build(result)

    assert report["has_improvement"]
    assert report["steps"][0]["iteration"] == 1


def test_zone_iterative_panel_import():
    from pini_desktop.ui.views.zone_iterative_panel import ZoneIterativePanel

    assert ZoneIterativePanel is not None
