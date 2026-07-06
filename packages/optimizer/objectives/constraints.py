from packages.optimizer.objective import OptimizationObjective
from packages.optimizer.constraints import ConstraintEngine


class ConstraintObjective(OptimizationObjective):
    name = "constraints"
    weight = 0.30

    def __init__(self):
        self.engine = ConstraintEngine()

    def evaluate(self, solution):
        conflicts = self.engine.evaluate(solution)
        value = max(0, 100 - len(conflicts) * 15)
        return value, {"conflicts": conflicts, "count": len(conflicts)}
