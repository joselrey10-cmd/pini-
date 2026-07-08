from pini_desktop.services.editor.optimization.chain_evaluator import SequenceScore
from pini_desktop.services.editor.optimization.move_sequence import MoveSequence, MoveStep
from pini_desktop.services.editor.optimization.sequence_detailed_report import SequenceDetailedReport
from pini_desktop.services.editor.optimization.sequence_explanation import SequenceExplanationBuilder


def make_score():
    seq = MoveSequence(steps=(
        MoveStep(1, 1, 2, 3, 1.5, "Mover A"),
        MoveStep(2, 2, 3, 4, 1.7, "Mover B"),
    ))
    return SequenceScore(sequence=seq, score=3.0, risk=0.35, recommendation="Cadena positiva")


def test_sequence_explanation_builder():
    explanation = SequenceExplanationBuilder().build(make_score())

    assert explanation.summary
    assert explanation.strengths
    assert explanation.risks
    assert explanation.recommendation


def test_sequence_detailed_report_text():
    text = SequenceDetailedReport().build_text(make_score())

    assert "Informe de cadena IA" in text
    assert "Pasos" in text
    assert "Recomendación" in text


def test_sequence_report_dialog_import():
    from pini_desktop.ui.views.sequence_report_dialog import SequenceReportDialog

    assert SequenceReportDialog is not None
