from pini_desktop.services.editor.optimization.alternative_generator import EditorAlternative
from pini_desktop.services.editor.optimization.alternative_preview import AlternativePreviewService
from pini_desktop.services.editor.optimization.candidate_builder import MoveCandidate


def test_alternative_preview_builds_text():
    alternative = EditorAlternative(
        title="Mover a martes",
        estimated_delta=1.5,
        estimated_score=82,
        explanation="Alternativa válida.",
        candidate=MoveCandidate(1, 2, 3, "Mover a martes"),
        bullets=("✔ Mejora el reparto.",),
    )

    text = AlternativePreviewService().build_text(alternative)

    assert "Destino" in text
    assert "Mejora estimada" in text
    assert "Motivos" in text


def test_alternative_preview_dialog_import():
    from pini_desktop.ui.views.alternative_preview_dialog import AlternativePreviewDialog

    assert AlternativePreviewDialog is not None
