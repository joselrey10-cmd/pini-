from pini_desktop.services.editor.optimization.local_optimizer import LocalOptimizationService


class DummyResult:
    def __init__(self, success=True, old_score=80, new_score=82):
        self.success = success
        self.old_score = old_score
        self.new_score = new_score
        self.messages = ()
        self.warnings = ()


def test_local_optimization_suggests_keep_when_score_improves():
    result = LocalOptimizationService().analyse_after_move(DummyResult(new_score=85))

    assert result.has_suggestions
    assert result.suggestions[0].action_type == "keep"


def test_local_optimization_suggests_review_when_score_drops():
    result = LocalOptimizationService().analyse_after_move(DummyResult(old_score=90, new_score=80))

    assert result.has_suggestions
    assert result.suggestions[0].action_type == "review"


def test_local_optimization_panel_import():
    from pini_desktop.ui.views.local_optimization_panel import LocalOptimizationPanel

    assert LocalOptimizationPanel is not None
