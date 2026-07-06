from dataclasses import dataclass

from .evaluator import ScheduleEvaluator


@dataclass(frozen=True)
class EngineEvaluationResult:
    score: float
    details: dict
    solution: object


class OptimizationEngine:
    def __init__(self, evaluator: ScheduleEvaluator | None = None):
        self.evaluator = evaluator or ScheduleEvaluator()

    def evaluate(self, solution) -> EngineEvaluationResult:
        score = self.evaluator.evaluate(solution)
        return EngineEvaluationResult(
            score=score.total,
            details=score.as_dict(),
            solution=solution,
        )
