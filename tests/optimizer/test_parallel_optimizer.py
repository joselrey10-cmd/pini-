from packages.optimizer.models import Session
from packages.optimizer.parallel import ParallelOptimizer
from packages.optimizer.parallel_report import ParallelOptimizationReport
from packages.optimizer.solution import Solution


def test_parallel_optimizer_returns_best_solution():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Luis", "2A", "Mate", "A2", 1, 2),
            Session("Marta", "3A", "Inglés", "A3", 2, 1),
            Session("Pedro", "4A", "EF", "Gimnasio", 2, 2),
        ]
    )

    result = ParallelOptimizer(workers=2, candidates_per_worker=3).optimize(solution)

    assert result.total_runs == 2
    assert result.best_name
    assert 0 <= result.best_score <= 100
    assert result.best_solution is not None


def test_parallel_report():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Luis", "2A", "Mate", "A2", 1, 2),
        ]
    )

    report = ParallelOptimizationReport().build(solution, workers=2, candidates_per_worker=2)

    assert report["workers"] == 2
    assert report["best_name"]
    assert len(report["runs"]) == 2
