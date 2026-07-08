from pini_desktop.services.editor.optimization.chain_evaluator import ChainEvaluator
from pini_desktop.services.editor.optimization.future_simulation import FutureSimulationEngine
from pini_desktop.services.editor.optimization.move_sequence import MoveSequence, MoveStep
from pini_desktop.services.editor.optimization.predictive_report import PredictiveSimulationReport
from pini_desktop.services.editor.optimization.predictive_sequence_evaluator import PredictiveSequenceEvaluator


def make_sequence():
    return MoveSequence(steps=(
        MoveStep(1, 1, 2, 3, 1.5, "Mover A"),
        MoveStep(2, 2, 3, 4, 1.4, "Mover B"),
    ))


def test_future_simulation_returns_impact():
    result = FutureSimulationEngine().simulate_sequence(make_sequence())

    assert result.impact.immediate_delta > 0
    assert isinstance(result.impact.future_delta, float)
    assert isinstance(result.is_recommended, bool)


def test_predictive_sequence_evaluator():
    sequence_score = ChainEvaluator().evaluate(make_sequence())
    predictive = PredictiveSequenceEvaluator().evaluate(sequence_score)

    assert predictive.predictive_score <= sequence_score.score
    assert predictive.recommendation


def test_predictive_report_text():
    sequence_score = ChainEvaluator().evaluate(make_sequence())
    predictive = PredictiveSequenceEvaluator().evaluate(sequence_score)
    text = PredictiveSimulationReport().build_text(predictive)

    assert "Simulación predictiva" in text
    assert "Riesgos" in text
    assert "Oportunidades" in text


def test_predictive_dialog_import():
    from pini_desktop.ui.views.predictive_simulation_dialog import PredictiveSimulationDialog

    assert PredictiveSimulationDialog is not None
