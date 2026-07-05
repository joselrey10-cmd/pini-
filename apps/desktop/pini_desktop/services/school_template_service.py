from dataclasses import dataclass

from pini_desktop.services.course_service import Course, CourseService
from pini_desktop.services.dynamic_rule_service import DynamicRuleService
from pini_desktop.services.room_service import RoomService
from pini_desktop.services.subject_service import SubjectService


@dataclass(frozen=True)
class TemplateResult:
    created_courses: int = 0
    created_subjects: int = 0
    created_rooms: int = 0
    created_rules: int = 0


class SchoolTemplateService:
    def __init__(self, database_path=None):
        self.course_service = CourseService(database_path) if database_path else CourseService()
        self.subject_service = SubjectService(database_path) if database_path else SubjectService()
        self.room_service = RoomService(database_path) if database_path else RoomService()
        self.rule_service = DynamicRuleService(database_path) if database_path else DynamicRuleService()

    def create_primary_template(self, groups: list[str] | None = None) -> TemplateResult:
        groups = groups or ["A"]
        return TemplateResult(
            created_courses=self._create_primary_courses(groups),
            created_subjects=self._seed_count(self.subject_service, "list_subjects", "seed_default_subjects"),
            created_rooms=self._seed_count(self.room_service, "list_rooms", "seed_default_rooms"),
            created_rules=self._seed_count(self.rule_service, "list_rules", "seed_center_rules"),
        )

    def _create_primary_courses(self, groups: list[str]) -> int:
        existing = {course.code for course in self.course_service.list_courses()}
        created = 0

        for level in range(1, 7):
            for group in groups:
                group = group.strip().upper()
                code = f"{level}{group}"
                if code in existing:
                    continue
                self.course_service.create_course(
                    Course(
                        id=None,
                        code=code,
                        stage="Primaria",
                        level=level,
                        group_name=group,
                        students=25,
                        tutor_teacher_id=None,
                    )
                )
                existing.add(code)
                created += 1

        return created

    def _seed_count(self, service, list_method: str, seed_method: str) -> int:
        before = len(getattr(service, list_method)())
        getattr(service, seed_method)()
        after = len(getattr(service, list_method)())
        return max(0, after - before)
