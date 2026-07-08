from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict

from .virtual_schedule import VirtualSchedule, VirtualSession


@dataclass(frozen=True)
class GlobalMetrics:
    sessions: int
    teacher_gaps: int
    course_gaps: int
    last_periods: int
    teacher_conflicts: int
    course_conflicts: int
    room_conflicts: int
    occupied_room_slots: int
    score: float

    @property
    def total_conflicts(self) -> int:
        return self.teacher_conflicts + self.course_conflicts + self.room_conflicts


class GlobalMetricsCalculator:
    """First global score for a virtual schedule.

    It favours schedules without hard conflicts, with fewer gaps and fewer last
    periods. The scoring is intentionally transparent and cheap so it can run in
    simulations many times.
    """

    def calculate(self, schedule: VirtualSchedule) -> GlobalMetrics:
        sessions = schedule.sessions()
        teacher_gaps = self._count_gaps(sessions, "teacher_id")
        course_gaps = self._count_gaps(sessions, "course_id")
        last_periods = sum(1 for item in sessions if item.period >= 6)
        teacher_conflicts = self._count_conflicts(sessions, "teacher_id")
        course_conflicts = self._count_conflicts(sessions, "course_id")
        room_conflicts = self._count_conflicts(sessions, "room_id")
        occupied_room_slots = len({(item.room_id, item.day, item.period) for item in sessions if item.room_id is not None})

        penalty = (
            teacher_conflicts * 12
            + course_conflicts * 12
            + room_conflicts * 10
            + teacher_gaps * 2
            + course_gaps * 2
            + last_periods * 0.5
        )
        score = round(max(0.0, min(100.0, 100.0 - penalty)), 2)

        return GlobalMetrics(
            sessions=len(sessions),
            teacher_gaps=teacher_gaps,
            course_gaps=course_gaps,
            last_periods=last_periods,
            teacher_conflicts=teacher_conflicts,
            course_conflicts=course_conflicts,
            room_conflicts=room_conflicts,
            occupied_room_slots=occupied_room_slots,
            score=score,
        )

    def _count_gaps(self, sessions: tuple[VirtualSession, ...], attr: str) -> int:
        grouped: dict[tuple[int | None, int], list[int]] = defaultdict(list)
        for session in sessions:
            entity = getattr(session, attr)
            if entity is not None:
                grouped[(entity, session.day)].append(session.period)

        gaps = 0
        for periods in grouped.values():
            ordered = sorted(set(periods))
            for first, second in zip(ordered, ordered[1:]):
                gaps += max(0, second - first - 1)
        return gaps

    def _count_conflicts(self, sessions: tuple[VirtualSession, ...], attr: str) -> int:
        grouped: dict[tuple[int | None, int, int], int] = defaultdict(int)
        for session in sessions:
            entity = getattr(session, attr)
            if entity is not None:
                grouped[(entity, session.day, session.period)] += 1
        return sum(max(0, count - 1) for count in grouped.values())
