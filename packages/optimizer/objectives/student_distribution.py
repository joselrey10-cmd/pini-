from packages.optimizer.objective import OptimizationObjective
from packages.optimizer.student_metrics import StudentDistributionAnalyzer


class StudentDistributionObjective(OptimizationObjective):
    name = "student_distribution"
    weight = 0.25

    def __init__(self):
        self.analyzer = StudentDistributionAnalyzer()

    def evaluate(self, solution):
        metrics = self.analyzer.analyse(solution)
        if not metrics:
            return 100, {"courses": 0}
        value = round(sum(item.distribution_score for item in metrics.values()) / len(metrics), 2)
        return value, {"courses": len(metrics)}
