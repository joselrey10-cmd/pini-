from pini_desktop.services.editor.optimization.chain_evaluator import ChainEvaluator
from pini_desktop.services.editor.optimization.move_sequence import MoveSequence, MoveStep
from pini_desktop.services.editor.optimization.predictive_sequence_ranker import PredictiveSequenceRanker
from pini_desktop.services.editor.optimization.predictive_sequence_evaluator import PredictiveSequenceEvaluator


def make_score(delta):
    seq = MoveSequence(steps=(MoveStep(1, 1, 2, 3, delta, "Mover"),))
    return PredictiveSequenceEvaluator().evaluate(ChainEvaluator().evaluate(seq))


def test_predictive_sequence_ranker_orders_items():
    items = [make_score(0.5), make_score(2.0), make_score(1.0)]
    ranked = PredictiveSequenceRanker().rank(items)

    assert ranked[0].predictive_score >= ranked[-1].predictive_score


def test_predictive_sequence_optimizer_import():
    from pini_desktop.services.editor.optimization.predictive_sequence_optimizer import PredictiveSequenceOptimizer

    assert PredictiveSequenceOptimizer is not None


def test_sequence_optimizer_panel_predictive_import():
    from pini_desktop.ui.views.sequence_optimizer_panel import SequenceOptimizerPanel

    assert SequenceOptimizerPanel is not None
