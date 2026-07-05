from .optimizer import Optimizer
from .teacher_metrics import TeacherMetricsAnalyzer


class QualityReport:
    def build(self, solution):
        evaluated = Optimizer(max_iterations=0).evaluate(solution)
        teacher_metrics = TeacherMetricsAnalyzer().analyse(evaluated)

        return {
            "score": evaluated.score,
            "conflicts": list(evaluated.conflicts),
            "sessions": len(evaluated.sessions),
            "teachers": {
                teacher: {
                    "gaps": metrics.gaps,
                    "last_periods": metrics.last_periods,
                    "max_daily_load": metrics.max_daily_load,
                    "overloaded_days": metrics.overloaded_days,
                    "compactness_score": metrics.compactness_score,
                }
                for teacher, metrics in teacher_metrics.items()
            },
        }
