from abc import ABC, abstractmethod


class OptimizationObjective(ABC):
    name = "objective"
    weight = 1.0

    @abstractmethod
    def evaluate(self, solution) -> tuple[float, dict]:
        """Return score 0-100 and optional details."""
        raise NotImplementedError
