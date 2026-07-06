from packages.optimizer.models import Session
from packages.optimizer.solution import Solution
from packages.optimizer.genetic import GeneticOptimizer
from packages.optimizer.search_report import SearchReport


def test_genetic_optimizer_returns_result():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Ana", "2A", "Mate", "A2", 1, 1),
            Session("Luis", "1A", "Mate", "A1", 1, 2),
            Session("Luis", "2A", "Lengua", "A2", 1, 2),
            Session("Marta", "3A", "Inglés", "A3", 2, 1),
            Session("Marta", "4A", "Inglés", "A4", 2, 1),
        ]
    )

    result = GeneticOptimizer(generations=3, population_size=8, seed=123).optimize(solution)

    assert result.best_score >= 0
    assert result.generations == 3
    assert result.population_size == 8
    assert result.solution is not None


def test_search_report_genetic_mode():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Luis", "2A", "Mate", "A2", 1, 2),
        ]
    )

    report = SearchReport().build(solution, max_iterations=20, mode="genetic")

    assert report["mode"] == "genetic"
    assert "generations" in report
    assert "mutations" in report
