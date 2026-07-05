from packages.optimizer.models import Session
from packages.optimizer.solution import Solution
from packages.optimizer.student_metrics import StudentDistributionAnalyzer
from packages.optimizer.optimizer import Optimizer


def test_student_distribution_detects_repetition_and_consecutive_subjects():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Luis", "1A", "Lengua", "A1", 1, 2),
            Session("Marta", "1A", "Lengua", "A1", 1, 3),
            Session("Juan", "1A", "Mate", "A1", 1, 4),
        ]
    )

    metrics = StudentDistributionAnalyzer().analyse(solution)

    assert metrics["1A"].repeated_subject_days == 1
    assert metrics["1A"].consecutive_same_subject == 2
    assert metrics["1A"].distribution_score < 100


def test_optimizer_rewards_better_student_distribution():
    balanced = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Luis", "1A", "Mate", "A1", 1, 2),
            Session("Marta", "1A", "Inglés", "A1", 1, 3),
        ]
    )

    concentrated = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Luis", "1A", "Lengua", "A1", 1, 2),
            Session("Marta", "1A", "Lengua", "A1", 1, 3),
        ]
    )

    optimizer = Optimizer(max_iterations=0)
    balanced_result = optimizer.evaluate(balanced)
    concentrated_result = optimizer.evaluate(concentrated)

    assert balanced_result.score > concentrated_result.score
