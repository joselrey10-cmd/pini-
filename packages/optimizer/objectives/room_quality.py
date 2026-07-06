from packages.optimizer.objective import OptimizationObjective
from packages.optimizer.room_metrics import RoomMetricsAnalyzer


class RoomQualityObjective(OptimizationObjective):
    name = "room_quality"
    weight = 0.20

    def __init__(self):
        self.analyzer = RoomMetricsAnalyzer()

    def evaluate(self, solution):
        metrics = self.analyzer.analyse(solution)
        if not metrics:
            return 100, {"rooms": 0}
        value = round(sum(item.score for item in metrics.values()) / len(metrics), 2)
        return value, {"rooms": len(metrics)}
