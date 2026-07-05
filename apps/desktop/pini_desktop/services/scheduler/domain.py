from dataclasses import dataclass


@dataclass(frozen=True)
class ScheduleAssignment:
    course_id: int
    subject_id: int
    weekly_sessions: int
    preferred_teacher_id: int | None
    required_room_type: str
    course_code: str
    subject_name: str


@dataclass(frozen=True)
class SchedulePeriod:
    day: int
    period: int
    is_after_break: bool


@dataclass(frozen=True)
class SchedulePlacement:
    course_id: int
    subject_id: int
    teacher_id: int | None
    room_id: int | None
    day: int
    period: int
    generated_by: str


@dataclass(frozen=True)
class ScheduleGenerationResult:
    placements: list[SchedulePlacement]
    warnings: list[str]

    @property
    def success(self) -> bool:
        return not self.warnings
