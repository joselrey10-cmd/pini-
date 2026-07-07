from pini_desktop.services.editor.optimization.local_optimizer import LocalOptimizationSuggestion
from pini_desktop.services.editor.optimization.suggestion_service import EditorSuggestionService


def test_informative_suggestion_is_not_applied():
    suggestion = LocalOptimizationSuggestion(
        title="Revisar",
        description="Sugerencia informativa",
        estimated_delta=1.0,
        action_type="review",
        payload={},
    )

    result = EditorSuggestionService().apply(suggestion)

    assert not result.success
    assert result.editor_result is None


def test_local_optimization_panel_has_apply_signal():
    from pini_desktop.ui.views.local_optimization_panel import LocalOptimizationPanel

    panel_class = LocalOptimizationPanel
    assert hasattr(panel_class, "suggestionApplied")
