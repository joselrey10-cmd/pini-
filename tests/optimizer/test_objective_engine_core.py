from packages.optimizer.engine import OptimizationEngine
from packages.optimizer.evaluator import ScheduleEvaluator
from packages.optimizer.models import Session
from packages.optimizer.solution import Solution


def test_schedule_evaluator_returns_objective_breakdown():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Luis", "2A", "Mate", "A2", 1, 2),
        ]
    )

    score = ScheduleEvaluator().evaluate(solution)

    assert 0 <= score.total <= 100
    assert len(score.objectives) >= 4
    assert solution.score == score.total


def test_optimization_engine_returns_details():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
        ]
    )

    result = OptimizationEngine().evaluate(solution)

    assert 0 <= result.score <= 100
    assert "objectives" in result.details
    assert result.solution is solution
