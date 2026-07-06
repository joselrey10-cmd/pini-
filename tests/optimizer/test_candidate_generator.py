from packages.optimizer.candidate_generator import CandidateGenerator
from packages.optimizer.candidate_report import CandidateGenerationReport
from packages.optimizer.models import Session
from packages.optimizer.solution import Solution


def test_candidate_generator_creates_candidates():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Luis", "2A", "Mate", "A2", 1, 2),
            Session("Marta", "3A", "Inglés", "A3", 2, 1),
        ]
    )

    result = CandidateGenerator(seed=1).generate(solution, count=5, swaps_per_candidate=2)

    assert len(result.candidates) == 5
    assert result.best_name
    assert result.best_solution is not None


def test_candidate_report_contains_ranking():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Luis", "2A", "Mate", "A2", 1, 2),
        ]
    )

    report = CandidateGenerationReport().build(solution, count=4)

    assert report["generated"] == 4
    assert report["best_name"]
    assert len(report["ranking"]) == 4
