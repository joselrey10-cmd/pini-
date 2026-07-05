from dataclasses import dataclass


@dataclass
class ScoreBreakdown:
    teacher_gaps: int = 0
    distribution: int = 0
    room_usage: int = 0
    constraints: int = 0
    total: float = 0


class Scorer:
    def evaluate(self, solution):
        conflicts = len(getattr(solution, "conflicts", []))
        constraints = max(0, 100 - conflicts * 15)
        teacher_gaps = max(0, 100 - self._teacher_gap_penalty(solution))
        distribution = max(0, 100 - self._distribution_penalty(solution))
        room_usage = max(0, 100 - self._room_penalty(solution))

        total = round(
            (constraints * 0.40)
            + (teacher_gaps * 0.25)
            + (distribution * 0.25)
            + (room_usage * 0.10),
            2,
        )

        solution.score = total
        return ScoreBreakdown(
            teacher_gaps=teacher_gaps,
            distribution=distribution,
            room_usage=room_usage,
            constraints=constraints,
            total=total,
        )

    def _teacher_gap_penalty(self, solution):
        penalty = 0
        by_teacher_day = {}
        for session in solution.sessions:
            by_teacher_day.setdefault((session.teacher, session.day), []).append(session.period)

        for periods in by_teacher_day.values():
            if len(periods) <= 1:
                continue
            ordered = sorted(periods)
            span = ordered[-1] - ordered[0] + 1
            gaps = span - len(set(ordered))
            penalty += gaps * 5

        return penalty

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
