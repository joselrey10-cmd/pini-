from .objective_registry import ObjectiveRegistry
from .score import EvaluationScore, ObjectiveScore
from .objectives import (
    ConstraintObjective,
    TeacherCompactnessObjective,
    StudentDistributionObjective,
    RoomQualityObjective,
)


class ScheduleEvaluator:
    def __init__(self, registry: ObjectiveRegistry | None = None):
        self.registry = registry or self.default_registry()

    @staticmethod
    def default_registry() -> ObjectiveRegistry:
        registry = ObjectiveRegistry()
        registry.register(ConstraintObjective())
        registry.register(TeacherCompactnessObjective())
        registry.register(StudentDistributionObjective())
        registry.register(RoomQualityObjective())
        return registry

    def evaluate(self, solution) -> EvaluationScore:
        objectives = self.registry.all()
        total_weight = sum(max(0, objective.weight) for objective in objectives) or 1

        scores = []
        total = 0.0

        for objective in objectives:
            value, details = objective.evaluate(solution)
            normalized_weight = max(0, objective.weight) / total_weight
            weighted = value * normalized_weight
            scores.append(
                ObjectiveScore(
                    name=objective.name,
                    value=round(value, 2),
                    weight=round(normalized_weight, 4),
                    weighted_value=round(weighted, 2),
                    details=details,
                )
            )
            total += weighted

        solution.score = round(total, 2)
        return EvaluationScore(total=round(total, 2), objectives=tuple(scores))
