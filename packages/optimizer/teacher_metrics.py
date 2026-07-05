from dataclasses import dataclass


@dataclass
class TeacherMetrics:
    gaps: int = 0
    last_periods: int = 0
    max_daily_load: int = 0
    overloaded_days: int = 0
    compactness_score: int = 100


class TeacherMetricsAnalyzer:
    def analyse(self, solution, max_daily_sessions: int = 5, last_period: int = 6) -> dict[str, TeacherMetrics]:
        by_teacher_day = {}

        for session in solution.sessions:
            if not session.teacher:
                continue
            by_teacher_day.setdefault((session.teacher, session.day), []).append(session.period)

        result: dict[str, TeacherMetrics] = {}

        for (teacher, _day), periods in by_teacher_day.items():
            metrics = result.setdefault(teacher, TeacherMetrics())
            ordered = sorted(periods)

            if len(ordered) > 1:
                span = ordered[-1] - ordered[0] + 1
                metrics.gaps += max(0, span - len(set(ordered)))

            metrics.last_periods += sum(1 for period in ordered if period == last_period)
            metrics.max_daily_load = max(metrics.max_daily_load, len(ordered))

            if len(ordered) > max_daily_sessions:
                metrics.overloaded_days += 1

        for metrics in result.values():
            penalty = metrics.gaps * 8 + metrics.last_periods * 3 + metrics.overloaded_days * 15
            metrics.compactness_score = max(0, 100 - penalty)

        return result
