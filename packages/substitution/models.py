from dataclasses import dataclass, field


@dataclass(frozen=True)
class Absence:
    teacher: str
    day: int
    period: int
    course: str = ""
    subject: str = ""
    room: str = ""
    required_speciality: str = ""


@dataclass(frozen=True)
class CandidateTeacher:
    name: str
    speciality: str = ""
    is_free: bool = True
    is_on_duty: bool = False
    same_building: bool = True
    can_move_support: bool = False
    breaks_important_support: bool = False
    current_task: str = ""


@dataclass
class SubstitutionProposal:
    candidate: CandidateTeacher
    score: int
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
