from PySide6.QtWidgets import QApplication

from pini_desktop.ui.editor.alternative_preview import AlternativePreviewDialog


app = QApplication.instance()
if app is None:
    app = QApplication([])


class FakeCandidate:
    session_id = 1
    target_day = 2
    target_period = 3


class FakeEstimatedScore:
    delta = 2.5
    candidate = FakeCandidate()


class FakeExplanation:
    summary = "Alternativa recomendable"
    bullets = ("✔ Mejora el reparto",)


class FakeAlternative:
    estimated_score = FakeEstimatedScore()
    explanation = FakeExplanation()


def test_alternative_preview_can_be_created():
    dialog = AlternativePreviewDialog(FakeAlternative())

    assert dialog.windowTitle() == "Vista previa de alternativa"