from packages.optimizer.models import Session
from packages.optimizer.solution import Solution
from packages.optimizer.simulated_annealing import SimulatedAnnealingOptimizer
from packages.optimizer.search_report import SearchReport


def test_simulated_annealing_returns_result():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Ana", "2A", "Mate", "A2", 1, 1),
            Session("Luis", "1A", "Mate", "A1", 1, 2),
            Session("Luis", "2A", "Lengua", "A2", 1, 2),
        ]
    )

    result = SimulatedAnnealingOptimizer(max_iterations=20, seed=123).optimize(solution)

    assert result.best_score >= 0
    assert result.iterations > 0
    assert result.solution is not None


def test_search_report_annealing_mode():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Luis", "2A", "Mate", "A2", 1, 2),
        ]
    )

    report = SearchReport().build(solution, max_iterations=5, mode="annealing")

    assert report["mode"] == "annealing"
    assert "best_score" in report
    assert "worse_moves" in report
