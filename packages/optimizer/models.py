from dataclasses import dataclass


@dataclass(frozen=True)
class Session:
    teacher: str
    course: str
    subject: str
    room: str
    day: int
    period: int
