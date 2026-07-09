from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from .virtual_schedule import VirtualSchedule


@dataclass(frozen=True)
class GlobalMetrics:
    sessions: int
    teacher_gaps: int
    course_gaps: int
    room_conflicts: int
    last_periods: int
    score: float

    @property
    def total_sessions(self) -> int:
        return self.sessions

    @property
    def conflicts(self) -> int:
        return self.room_conflicts

    @property
    def gaps(self) -> int:
        return self.teacher_gaps + self.course_gaps


class GlobalMetricsCalculator:
    """Calcula métricas globales básicas sobre un VirtualSchedule."""

    def calculate(self, virtual_schedule) -> GlobalMetrics:
        if not isinstance(virtual_schedule, VirtualSchedule):
            virtual_schedule = VirtualSchedule.from_schedule(virtual_schedule)

        sessions = tuple(virtual_schedule.sessions())
        teacher_gaps = self._count_gaps_by(sessions, "teacher_id")
        course_gaps = self._count_gaps_by(sessions, "course_id")
        room_conflicts = self._count_room_conflicts(sessions)
        last_periods = sum(1 for session in sessions if session.period >= 6)

        score = 100.0
        score -= teacher_gaps * 3
        score -= course_gaps * 2
        score -= room_conflicts * 10
        score -= last_periods * 1

        return GlobalMetrics(
            sessions=len(sessions),
            teacher_gaps=teacher_gaps,
            course_gaps=course_gaps,
            room_conflicts=room_conflicts,
            last_periods=last_periods,
            score=round(max(0.0, min(100.0, score)), 2),
        )

    def _count_gaps_by(self, sessions, attr: str) -> int:
        grouped = defaultdict(list)
        for session in sessions:
            entity_id = getattr(session, attr, None)
            if entity_id is not None:
                grouped[(entity_id, session.day)].append(session.period)

        gaps = 0
        for periods in grouped.values():
            ordered = sorted(set(periods))
            if len(ordered) < 2:
                continue
            gaps += max(0, ordered[-1] - ordered[0] + 1 - len(ordered))
        return gaps

    def _count_room_conflicts(self, sessions) -> int:
        grouped = defaultdict(list)
        for session in sessions:
            if session.room_id is not None:
                grouped[(session.room_id, session.day, session.period)].append(session.id)
        return sum(max(0, len(items) - 1) for items in grouped.values())
