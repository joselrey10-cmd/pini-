from dataclasses import dataclass, field


@dataclass(frozen=True)
class ObjectiveScore:
    name: str
    value: float
    weight: float
    weighted_value: float
    details: dict = field(default_factory=dict)


@dataclass(frozen=True)
class EvaluationScore:
    total: float
    objectives: tuple[ObjectiveScore, ...] = ()

    def as_dict(self) -> dict:
        return {
            "total": self.total,
            "objectives": [
                {
                    "name": item.name,
                    "value": item.value,
                    "weight": item.weight,
                    "weighted_value": item.weighted_value,
                    "details": item.details,
                }
                for item in self.objectives
            ],
        }
