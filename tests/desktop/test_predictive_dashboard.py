from pini_desktop.services.editor.optimization.chain_evaluator import ChainEvaluator
from pini_desktop.services.editor.optimization.move_sequence import MoveSequence, MoveStep
from pini_desktop.services.editor.optimization.predictive_dashboard import PredictiveDashboardBuilder
from pini_desktop.services.editor.optimization.predictive_dashboard_report import PredictiveDashboardReport
from pini_desktop.services.editor.optimization.predictive_sequence_evaluator import PredictiveSequenceEvaluator


def make_predictive(delta):
    seq = MoveSequence(steps=(MoveStep(1, 1, 2, 3, delta, "Mover"),))
    sequence_score = ChainEvaluator().evaluate(seq)
    return PredictiveSequenceEvaluator().evaluate(sequence_score)


def test_predictive_dashboard_selects_best():
    dashboard = PredictiveDashboardBuilder().build([make_predictive(0.5), make_predictive(2.0)])

    assert dashboard.has_items
    assert dashboard.best.predictive_score >= dashboard.items[-1].predictive_score


def test_predictive_dashboard_report_text():
    text = PredictiveDashboardReport().build_text([make_predictive(1.0)])

    assert "Resumen predictivo" in text
    assert "Ranking" in text


def test_predictive_dashboard_dialog_import():
    from pini_desktop.ui.views.predictive_dashboard_dialog import PredictiveDashboardDialog

    assert PredictiveDashboardDialog is not None
