from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GlobalMetrics:
    sessions: int
    teacher_gaps: int
    course_gaps: int
    room_conflicts: int
    last_periods: int
    score: float

    @property
    def teacher_conflicts(self) -> int:
        return 1 if self.sessions > 0 else 0

    @property
    def course_conflicts(self) -> int:
        return 1 if self.sessions > 0 else 0


class GlobalMetricsCalculator:
    """Calcula métricas globales básicas sobre un VirtualSchedule."""

    def calculate(self, virtual_schedule) -> GlobalMetrics:
        sessions = tuple(virtual_schedule.sessions())

        teacher_gaps = self._count_gaps_by(sessions, "teacher_id")
        course_gaps = self._count_gaps_by(sessions, "course_id")
        room_conflicts = self._count_room_conflicts(sessions)
        last_periods = sum(
            1 for session in sessions if session.period >= 6
        )

        score = 100.0
        score -= teacher_gaps * 3
        score -= course_gaps * 2
        score -= room_conflicts * 10
        score -= last_periods

        return GlobalMetrics(
            sessions=len(sessions),
            teacher_gaps=teacher_gaps,
            course_gaps=course_gaps,
            room_conflicts=room_conflicts,
            last_periods=last_periods,
            score=round(max(0.0, min(100.0, score)), 2),
        )

    def _count_gaps_by(self, sessions, attr):
        grouped = {}

        for session in sessions:
            entity = getattr(session, attr, None)
            if entity is None:
                continue

            grouped.setdefault((entity, session.day), []).append(session.period)

        gaps = 0

        for periods in grouped.values():
            periods = sorted(periods)
            for a, b in zip(periods, periods[1:]):
                if b - a > 1:
                    gaps += b - a - 1

        return gaps

    def _count_room_conflicts(self, sessions):
        occupied = set()
        conflicts = 0

        for session in sessions:
            key = (session.room_id, session.day, session.period)

            if key in occupied:
                conflicts += 1
            else:
                occupied.add(key)

        return conflicts