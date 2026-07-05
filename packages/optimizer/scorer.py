from dataclasses import dataclass

from .teacher_metrics import TeacherMetricsAnalyzer


@dataclass
class ScoreBreakdown:
    teacher_gaps: int = 0
    distribution: int = 0
    room_usage: int = 0
    constraints: int = 0
    teacher_compactness: int = 0
    total: float = 0


class Scorer:
    def __init__(self):
        self.teacher_analyzer = TeacherMetricsAnalyzer()

    def evaluate(self, solution):
        conflicts = len(getattr(solution, "conflicts", []))
        constraints = max(0, 100 - conflicts * 15)
        teacher_compactness = self._teacher_compactness_score(solution)
        distribution = max(0, 100 - self._distribution_penalty(solution))
        room_usage = max(0, 100 - self._room_penalty(solution))

        total = round(
            (constraints * 0.35)
            + (teacher_compactness * 0.35)
            + (distribution * 0.20)
            + (room_usage * 0.10),
            2,
        )

        solution.score = total
        return ScoreBreakdown(
            teacher_gaps=teacher_compactness,
            distribution=distribution,
            room_usage=room_usage,
            constraints=constraints,
            teacher_compactness=teacher_compactness,
            total=total,
        )

    def _teacher_compactness_score(self, solution):
        metrics = self.teacher_analyzer.analyse(solution)
        if not metrics:
            return 100
        return round(sum(item.compactness_score for item in metrics.values()) / len(metrics))

    def _distribution_penalty(self, solution):
        penalty = 0
        by_course_subject_day = {}
        for session in solution.sessions:
            key = (session.course, session.subject, session.day)
            by_course_subject_day[key] = by_course_subject_day.get(key, 0) + 1

        for count in by_course_subject_day.values():
            if count > 2:
                penalty += (count - 2) * 8

        return penalty

    def _room_penalty(self, solution):
        return 0
