from packages.optimizer.models import Session
from packages.optimizer.solution import Solution
from packages.optimizer.local_search import HillClimbingOptimizer
from packages.optimizer.search_report import SearchReport


def test_hill_climbing_returns_valid_result():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Ana", "2A", "Mate", "A2", 1, 1),
            Session("Luis", "1A", "Mate", "A1", 1, 2),
            Session("Luis", "2A", "Lengua", "A2", 1, 2),
        ]
    )

    result = HillClimbingOptimizer(max_iterations=20).optimize(solution)

    assert result.final_score >= result.initial_score
    assert result.iterations >= 0
    assert result.solution is not None


def test_search_report_has_expected_fields():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Luis", "2A", "Mate", "A2", 1, 2),
        ]
    )

    report = SearchReport().build(solution, max_iterations=10)

    assert "initial_score" in report
    assert "final_score" in report
    assert "accepted_moves" in report
