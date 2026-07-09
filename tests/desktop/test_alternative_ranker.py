from pini_desktop.services.editor.optimization.alternative_ranker import (
    AlternativeRanker,
)


class FakeEstimated:
    def __init__(self, delta, conflicts):
        self.delta = delta
        self.conflicts = conflicts


class FakeAlternative:
    def __init__(self, delta, conflicts):
        self.estimated_score = FakeEstimated(delta, conflicts)


def test_rank_orders_by_score():
    alternatives = [
        FakeAlternative(1.2, 0),
        FakeAlternative(3.0, 2),
        FakeAlternative(2.7, 0),
    ]

    ranked = AlternativeRanker().rank(alternatives)

    assert ranked[0].estimated_score.delta == 3.0


def test_best_returns_first():
    alternatives = [
        FakeAlternative(0.8, 0),
        FakeAlternative(5.1, 1),
    ]

    best = AlternativeRanker().best(alternatives)

    assert best.estimated_score.delta == 5.1