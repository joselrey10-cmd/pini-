from pathlib import Path

from pini_desktop.services.course_service import CourseService
from pini_desktop.services.dynamic_rule_service import DynamicRuleService
from pini_desktop.services.room_service import RoomService
from pini_desktop.services.school_template_service import SchoolTemplateService
from pini_desktop.services.subject_service import SubjectService


def test_primary_school_template_creates_base_data(tmp_path: Path):
    db = tmp_path / "test_pini.db"

    service = SchoolTemplateService(database_path=db)
    result = service.create_primary_template(["A", "B"])

    assert result.created_courses == 12
    assert len(CourseService(database_path=db).list_courses()) == 12
    assert len(SubjectService(database_path=db).list_subjects()) >= 8
    assert len(RoomService(database_path=db).list_rooms()) >= 8
    assert len(DynamicRuleService(database_path=db).list_rules()) >= 3
