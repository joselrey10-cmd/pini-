from pini_desktop.services.editor.optimization.alternative_generator import EditorAlternative
from pini_desktop.services.editor.optimization.alternative_ranker import AlternativeRanker
from pini_desktop.services.editor.optimization.candidate_builder import MoveCandidate


def alt(delta, score, day, period):
    candidate = MoveCandidate(
        session_id=1,
        day=day,
        period=period,
        title=f"{day}-{period}",
    )
    return EditorAlternative(
        title=candidate.title,
        estimated_delta=delta,
        estimated_score=score,
        explanation="",
        candidate=candidate,
    )


def test_ranker_orders_by_delta():
    ranked = AlternativeRanker().rank(
        [
            alt(0.2, 80.2, 1, 1),
            alt(1.5, 81.5, 2, 2),
            alt(0.8, 80.8, 3, 3),
        ]
    )

    assert ranked[0].estimated_delta == 1.5


def test_ranker_removes_duplicate_destinations():
    ranked = AlternativeRanker().rank(
        [
            alt(1.0, 81, 1, 1),
            alt(1.2, 82, 1, 1),
            alt(0.5, 80.5, 2, 2),
        ],
        limit=5,
    )

    destinations = {(item.candidate.day, item.candidate.period) for item in ranked}
    assert len(destinations) == len(ranked)


def test_generator_uses_ranker_limit():
    from pini_desktop.services.editor.optimization.alternative_generator import AlternativeGenerator

    alternatives = AlternativeGenerator().generate_for_session(1, 2, 3, limit=2)

    assert len(alternatives) <= 2
    assert alternatives[0].estimated_delta >= alternatives[-1].estimated_delta
