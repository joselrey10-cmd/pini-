from pini_desktop.services.editor.optimization.alternative_comparator import AlternativeComparator
from pini_desktop.services.editor.optimization.alternative_generator import EditorAlternative
from pini_desktop.services.editor.optimization.candidate_builder import MoveCandidate


def make_alt(title, delta, score):
    return EditorAlternative(
        title=title,
        estimated_delta=delta,
        estimated_score=score,
        explanation="",
        candidate=MoveCandidate(1, 1, 1, title),
        bullets=("✔ Mejora el reparto entre días.",),
    )


def test_alternative_comparator_selects_best():
    alternatives = [
        make_alt("A", 0.5, 80.5),
        make_alt("B", 2.0, 82),
        make_alt("C", 1.0, 81),
    ]

    result = AlternativeComparator().compare(alternatives)

    assert result.has_best
    assert result.best.alternative.title == "B"
    assert result.best.rank == 1
    assert result.best.strengths


def test_alternative_report_builds_dict():
    from pini_desktop.services.editor.optimization.alternative_report import AlternativeComparisonReport

    report = AlternativeComparisonReport().build([make_alt("A", 1.0, 81)])

    assert report["has_best"]
    assert report["best_title"] == "A"
    assert report["items"][0]["rank"] == 1
