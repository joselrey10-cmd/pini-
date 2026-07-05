from dataclasses import dataclass


@dataclass
class CourseMetrics:
    repeated_subject_days: int = 0
    overloaded_days: int = 0
    consecutive_same_subject: int = 0
    first_last_imbalance: int = 0
    distribution_score: int = 100


class StudentDistributionAnalyzer:
    def analyse(self, solution, max_same_subject_per_day: int = 2, max_sessions_per_day: int = 6) -> dict[str, CourseMetrics]:
        by_course_day = {}
        for session in solution.sessions:
            if not session.course:
                continue
            by_course_day.setdefault((session.course, session.day), []).append(session)

        result: dict[str, CourseMetrics] = {}

        for (course, _day), sessions in by_course_day.items():
            metrics = result.setdefault(course, CourseMetrics())
            ordered = sorted(sessions, key=lambda item: item.period)

            subject_counts = {}
            for session in ordered:
                subject_counts[session.subject] = subject_counts.get(session.subject, 0) + 1

            for count in subject_counts.values():
                if count > max_same_subject_per_day:
                    metrics.repeated_subject_days += count - max_same_subject_per_day

            if len(ordered) > max_sessions_per_day:
                metrics.overloaded_days += 1

            for previous, current in zip(ordered, ordered[1:]):
                if previous.subject == current.subject:
                    metrics.consecutive_same_subject += 1

            first_subjects = [s.subject for s in ordered if s.period == 1]
            last_subjects = [s.subject for s in ordered if s.period == max_sessions_per_day]
            metrics.first_last_imbalance += max(0, len(last_subjects) - len(first_subjects))

        for metrics in result.values():
            penalty = (
                metrics.repeated_subject_days * 10
                + metrics.overloaded_days * 15
                + metrics.consecutive_same_subject * 8
                + metrics.first_last_imbalance * 3
            )
            metrics.distribution_score = max(0, 100 - penalty)

        return result
