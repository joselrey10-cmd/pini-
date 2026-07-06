from packages.optimizer.comparator import SolutionComparator
from packages.optimizer.comparison_report import SolutionComparisonReport
from packages.optimizer.models import Session
from packages.optimizer.solution import Solution


def test_solution_comparator_orders_by_score():
    good = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Luis", "2A", "Mate", "A2", 1, 2),
        ]
    )
    bad = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Ana", "2A", "Mate", "A2", 1, 1),
        ]
    )

    result = SolutionComparator().compare({"buena": good, "mala": bad})

    assert result.has_winner
    assert result.items[0].score >= result.items[1].score
    assert result.items[0].rank == 1


def test_comparison_report():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
        ]
    )

    report = SolutionComparisonReport().build({"solución 1": solution})

    assert report["best_name"] == "solución 1"
    assert report["items"][0]["rank"] == 1
