from dataclasses import dataclass, field


@dataclass(frozen=True)
class TeacherImport:
    code: str
    name: str
    surname: str
    speciality: str = ""
    weekly_hours: int = 25
    role: str = ""


@dataclass(frozen=True)
class CourseImport:
    code: str
    stage: str
    level: int
    group_name: str
    students: int = 25


@dataclass(frozen=True)
class SubjectImport:
    code: str
    name: str
    weekly_sessions: int = 1
    speciality: str = ""
    room_type: str = "Ordinaria"


@dataclass(frozen=True)
class RoomImport:
    code: str
    name: str
    room_type: str = "Ordinaria"
    capacity: int = 25


@dataclass(frozen=True)
class SchoolConfigurationImport:
    center_name: str = ""
    center_code: str = ""
    locality: str = ""
    province: str = ""
    sessions_per_day: int = 6
    session_duration_minutes: int = 45
    break_after_period: int = 3
    break_duration_minutes: int = 30
    start_time: str = "09:00"


@dataclass(frozen=True)
class ImportPackage:
    teachers: tuple[TeacherImport, ...] = ()
    courses: tuple[CourseImport, ...] = ()
    subjects: tuple[SubjectImport, ...] = ()
    rooms: tuple[RoomImport, ...] = ()
    configuration: SchoolConfigurationImport | None = None
    source: str = "manual"
    metadata: dict = field(default_factory=dict)
