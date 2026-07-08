from pini_desktop.services.editor.optimization.chain_builder import ChainBuilder, ChainBuildConfig
from pini_desktop.services.editor.optimization.chain_evaluator import ChainEvaluator
from pini_desktop.services.editor.optimization.move_sequence import MoveSequence, MoveStep
from pini_desktop.services.editor.optimization.sequence_report import SequenceOptimizationReport
from pini_desktop.services.editor.optimization.zone_definition import ZoneDefinition
from pini_desktop.services.editor.optimization.zone_optimizer import ZoneOptimizationSuggestion


def test_move_sequence_accumulates_delta():
    seq = MoveSequence(steps=(
        MoveStep(1, 10, 1, 2, 1.5, "A"),
        MoveStep(2, 11, 2, 3, 2.0, "B"),
    ))

    assert seq.length == 2
    assert seq.estimated_delta == 3.5
    assert seq.session_ids == (10, 11)


def test_chain_builder_builds_sequences_without_repeating_session():
    suggestions = (
        ZoneOptimizationSuggestion(1, 1, 2, 1.0, "A"),
        ZoneOptimizationSuggestion(2, 2, 3, 1.5, "B"),
        ZoneOptimizationSuggestion(3, 3, 4, 0.7, "C"),
    )

    chains = ChainBuilder().build(suggestions, ChainBuildConfig(max_depth=2, max_branching=3))

    assert chains
    assert all(len(set(chain.session_ids)) == chain.length for chain in chains)
    assert chains[0].estimated_delta >= chains[-1].estimated_delta


def test_chain_evaluator_scores_sequence():
    seq = MoveSequence(steps=(
        MoveStep(1, 1, 1, 2, 2.0, "A"),
        MoveStep(2, 2, 2, 3, 2.0, "B"),
    ))

    score = ChainEvaluator().evaluate(seq)

    assert score.score > 0
    assert score.recommendation


def test_sequence_report_builds_dict():
    from pini_desktop.services.editor.optimization.sequence_optimizer import SequenceOptimizationResult
    from pini_desktop.services.editor.optimization.chain_evaluator import SequenceScore

    zone = ZoneDefinition("teacher", entity_id=1)
    seq = MoveSequence(steps=(MoveStep(1, 1, 1, 2, 1.0, "A"),))
    result = SequenceOptimizationResult(zone=zone, sequences=(SequenceScore(seq, 1.0, 0.1, "OK"),))

    report = SequenceOptimizationReport().build(result)

    assert report["has_sequences"]
    assert report["sequences"][0]["steps"][0]["session_id"] == 1
