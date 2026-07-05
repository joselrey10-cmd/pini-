from dataclasses import dataclass, field
from copy import deepcopy

from .models import Session


@dataclass
class Solution:
    sessions: list[Session] = field(default_factory=list)
    score: float = 0.0
    conflicts: list[str] = field(default_factory=list)

    def copy(self) -> "Solution":
        return deepcopy(self)

    def with_swapped_sessions(self, first_index: int, second_index: int) -> "Solution":
        new_solution = self.copy()
        sessions = list(new_solution.sessions)

        first = sessions[first_index]
        second = sessions[second_index]

        sessions[first_index] = Session(
            teacher=first.teacher,
            course=first.course,
            subject=first.subject,
            room=first.room,
            day=second.day,
            period=second.period,
        )
        sessions[second_index] = Session(
            teacher=second.teacher,
            course=second.course,
            subject=second.subject,
            room=second.room,
            day=first.day,
            period=first.period,
        )

        new_solution.sessions = sessions
        return new_solution
