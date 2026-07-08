from pini_desktop.services.editor.optimization.alternative_apply_service import AlternativeApplyService
from pini_desktop.services.editor.optimization.alternative_generator import EditorAlternative
from pini_desktop.services.editor.optimization.candidate_builder import MoveCandidate


def test_alternative_apply_service_can_be_created():
    service = AlternativeApplyService()
    assert service is not None


def test_alternatives_panel_has_signal():
    from pini_desktop.ui.views.alternatives_panel import AlternativesPanel

    assert hasattr(AlternativesPanel, "alternativeApplied")


def test_schedule_matrix_view_imports_alternatives_panel():
    from pini_desktop.ui.views.schedule_matrix_view import ScheduleMatrixView

    assert ScheduleMatrixView is not None
