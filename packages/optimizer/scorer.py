from dataclasses import dataclass

from .teacher_metrics import TeacherMetricsAnalyzer
from .student_metrics import StudentDistributionAnalyzer


@dataclass
class ScoreBreakdown:
    teacher_gaps: int = 0
    distribution: int = 0
    room_usage: int = 0
    constraints: int = 0
    teacher_compactness: int = 0
    student_distribution: int = 0
    total: float = 0


class Scorer:
    def __init__(self):
        self.teacher_analyzer = TeacherMetricsAnalyzer()
        self.student_analyzer = StudentDistributionAnalyzer()

    def evaluate(self, solution):
        conflicts = len(getattr(solution, "conflicts", []))
        constraints = max(0, 100 - conflicts * 15)
        teacher_compactness = self._teacher_compactness_score(solution)
        student_distribution = self._student_distribution_score(solution)
        room_usage = max(0, 100 - self._room_penalty(solution))

        total = round(
            (constraints * 0.30)
            + (teacher_compactness * 0.30)
            + (student_distribution * 0.30)
            + (room_usage * 0.10),
            2,
        )

        solution.score = total
        return ScoreBreakdown(
            teacher_gaps=teacher_compactness,
            distribution=student_distribution,
            room_usage=room_usage,
            constraints=constraints,
            teacher_compactness=teacher_compactness,
            student_distribution=student_distribution,
            total=total,
        )

    def _teacher_compactness_score(self, solution):
        metrics = self.teacher_analyzer.analyse(solution)
        if not metrics:
            return 100
        return round(sum(item.compactness_score for item in metrics.values()) / len(metrics))

    def _student_distribution_score(self, solution):
        metrics = self.student_analyzer.analyse(solution)
        if not metrics:
            return 100
        return round(sum(item.distribution_score for item in metrics.values()) / len(metrics))

    def _room_penalty(self, solution):
        return 0
