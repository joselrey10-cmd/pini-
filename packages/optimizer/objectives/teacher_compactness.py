from packages.optimizer.objective import OptimizationObjective
from packages.optimizer.teacher_metrics import TeacherMetricsAnalyzer


class TeacherCompactnessObjective(OptimizationObjective):
    name = "teacher_compactness"
    weight = 0.25

    def __init__(self):
        self.analyzer = TeacherMetricsAnalyzer()

    def evaluate(self, solution):
        metrics = self.analyzer.analyse(solution)
        if not metrics:
            return 100, {"teachers": 0}
        value = round(sum(item.compactness_score for item in metrics.values()) / len(metrics), 2)
        return value, {"teachers": len(metrics)}
