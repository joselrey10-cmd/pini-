from .optimizer import Optimizer
from .teacher_metrics import TeacherMetricsAnalyzer
from .student_metrics import StudentDistributionAnalyzer


class QualityReport:
    def build(self, solution):
        evaluated = Optimizer(max_iterations=0).evaluate(solution)
        teacher_metrics = TeacherMetricsAnalyzer().analyse(evaluated)
        course_metrics = StudentDistributionAnalyzer().analyse(evaluated)

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
            "courses": {
                course: {
                    "repeated_subject_days": metrics.repeated_subject_days,
                    "overloaded_days": metrics.overloaded_days,
                    "consecutive_same_subject": metrics.consecutive_same_subject,
                    "first_last_imbalance": metrics.first_last_imbalance,
                    "distribution_score": metrics.distribution_score,
                }
                for course, metrics in course_metrics.items()
            },
        }
