from packages.optimizer.models import Session
from packages.optimizer.solution import Solution
from packages.optimizer.teacher_metrics import TeacherMetricsAnalyzer
from packages.optimizer.optimizer import Optimizer


def test_teacher_metrics_detect_gaps_and_last_periods():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Ana", "2A", "Mate", "A2", 1, 3),
            Session("Ana", "3A", "Inglés", "A3", 1, 6),
        ]
    )

    metrics = TeacherMetricsAnalyzer().analyse(solution)

    assert metrics["Ana"].gaps == 2
    assert metrics["Ana"].last_periods == 1
    assert metrics["Ana"].compactness_score < 100


def test_optimizer_scores_teacher_compactness():
    compact = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Ana", "2A", "Mate", "A2", 1, 2),
        ]
    )

    with_gap = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Ana", "2A", "Mate", "A2", 1, 5),
        ]
    )

    optimizer = Optimizer(max_iterations=0)
    compact_result = optimizer.evaluate(compact)
    gap_result = optimizer.evaluate(with_gap)

    assert compact_result.score > gap_result.score
