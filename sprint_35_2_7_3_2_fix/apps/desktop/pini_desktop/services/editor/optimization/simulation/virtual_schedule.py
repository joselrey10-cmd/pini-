from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class VirtualSession:
    """Representación en memoria de una sesión de horario."""

    id: int
    course_id: int | None
    subject_id: int | None
    teacher_id: int | None
    room_id: int | None
    day: int
    period: int
    metadata: Mapping[str, Any] | None = None

    @classmethod
    def from_object(cls, value: object) -> "VirtualSession":
        if isinstance(value, VirtualSession):
            return value

        if isinstance(value, Mapping):
            getter = value.get
        else:
            getter = lambda name, default=None: getattr(value, name, default)

        session_id = getter("id", None)
        if session_id is None:
            session_id = getter("session_id", None)
        if session_id is None:
            raise ValueError("La sesión virtual necesita id o session_id.")

        return cls(
            id=int(session_id),
            course_id=getter("course_id", None),
            subject_id=getter("subject_id", None),
            teacher_id=getter("teacher_id", None),
            room_id=getter("room_id", None),
            day=int(getter("day")),
            period=int(getter("period")),
            metadata=dict(getter("metadata", {}) or {}),
        )

    def moved_to(self, day: int, period: int) -> "VirtualSession":
        return replace(self, day=int(day), period=int(period))


class VirtualSchedule:
    """Copia modificable del horario, sin tocar el horario original."""

    def __init__(self, sessions: Iterable[VirtualSession | object]):
        parsed = [VirtualSession.from_object(item) for item in sessions]
        self._initial = {item.id: item for item in parsed}
        self._sessions = dict(self._initial)

    @classmethod
    def from_sessions(cls, sessions: Iterable[VirtualSession | object]) -> "VirtualSchedule":
        return cls(sessions)

    @classmethod
    def from_schedule(cls, schedule: object) -> "VirtualSchedule":
        if isinstance(schedule, VirtualSchedule):
            return schedule.clone()
        if isinstance(schedule, Mapping):
            sessions = schedule.get("sessions", schedule.values())
        else:
            sessions = getattr(schedule, "sessions", schedule)
        if callable(sessions):
            sessions = sessions()
        return cls(sessions)

    def clone(self) -> "VirtualSchedule":
        return VirtualSchedule(self.sessions())

    def reset(self) -> None:
        self._sessions = dict(self._initial)

    def sessions(self) -> tuple[VirtualSession, ...]:
        return tuple(sorted(self._sessions.values(), key=lambda item: (item.day, item.period, item.id)))

    def get_session(self, session_id: int) -> VirtualSession:
        try:
            return self._sessions[int(session_id)]
        except KeyError as exc:
            raise ValueError(f"No existe la sesión virtual {session_id}.") from exc

    def move_session(self, session_id: int, day: int, period: int) -> VirtualSession:
        session = self.get_session(session_id)
        updated = session.moved_to(day, period)
        self._sessions[session.id] = updated
        return updated

    def swap_sessions(self, first_session_id: int, second_session_id: int) -> tuple[VirtualSession, VirtualSession]:
        first = self.get_session(first_session_id)
        second = self.get_session(second_session_id)
        updated_first = first.moved_to(second.day, second.period)
        updated_second = second.moved_to(first.day, first.period)
        self._sessions[first.id] = updated_first
        self._sessions[second.id] = updated_second
        return updated_first, updated_second

    def teacher_schedule(self, teacher_id: int) -> tuple[VirtualSession, ...]:
        return tuple(item for item in self.sessions() if item.teacher_id == teacher_id)

    def course_schedule(self, course_id: int) -> tuple[VirtualSession, ...]:
        return tuple(item for item in self.sessions() if item.course_id == course_id)

    def room_schedule(self, room_id: int) -> tuple[VirtualSession, ...]:
        return tuple(item for item in self.sessions() if item.room_id == room_id)

    def by_slot(self, day: int, period: int) -> tuple[VirtualSession, ...]:
        return tuple(item for item in self.sessions() if item.day == day and item.period == period)
