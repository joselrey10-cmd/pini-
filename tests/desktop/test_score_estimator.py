from pini_desktop.services.editor.optimization.candidate_builder import MoveCandidate
from pini_desktop.services.editor.optimization.score_estimator import ScoreEstimator


def test_score_estimator_returns_delta_and_reasons():
    candidate = MoveCandidate(
        session_id=1,
        day=2,
        period=2,
        title="Mover",
    )

    score = ScoreEstimator().estimate(candidate, current_day=2, current_period=3, current_score=80)

    assert score.estimated_score >= 80
    assert score.delta >= 0
    assert score.reasons


def test_score_estimator_penalizes_last_period():
    candidate = MoveCandidate(
        session_id=1,
        day=2,
        period=6,
        title="Mover",
    )

    score = ScoreEstimator().estimate(candidate, current_day=2, current_period=5, current_score=80)

    assert score.estimated_score <= 81


def test_alternative_generator_uses_estimator():
    from pini_desktop.services.editor.optimization.alternative_generator import AlternativeGenerator

    alternatives = AlternativeGenerator().generate_for_session(1, 2, 3, limit=3, current_score=75)

    assert alternatives
    assert alternatives[0].estimated_score >= 75
    assert alternatives[0].reasons
