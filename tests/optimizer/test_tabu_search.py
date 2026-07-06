from packages.optimizer.models import Session
from packages.optimizer.solution import Solution
from packages.optimizer.tabu_search import TabuSearchOptimizer
from packages.optimizer.search_report import SearchReport


def test_tabu_search_returns_result():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Ana", "2A", "Mate", "A2", 1, 1),
            Session("Luis", "1A", "Mate", "A1", 1, 2),
            Session("Luis", "2A", "Lengua", "A2", 1, 2),
        ]
    )

    result = TabuSearchOptimizer(max_iterations=20, tabu_size=5).optimize(solution)

    assert result.best_score >= 0
    assert result.iterations >= 0
    assert result.solution is not None


def test_search_report_tabu_mode():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Luis", "2A", "Mate", "A2", 1, 2),
        ]
    )

    report = SearchReport().build(solution, max_iterations=5, mode="tabu")

    assert report["mode"] == "tabu"
    assert "best_score" in report
    assert "tabu_skips" in report
