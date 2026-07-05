from pathlib import Path

from pini_desktop.services.excel_import_service import ExcelImportService
from pini_desktop.services.course_subject_service import CourseSubjectService
from pini_desktop.services.availability_service import AvailabilityService, AvailabilityStatus
from pini_desktop.services.teacher_service import TeacherService


def test_advanced_excel_import_template_and_import(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    template = tmp_path / "plantilla_completa.xlsx"

    service = ExcelImportService(database_path=db)
    service.create_template(template)
    result = service.import_workbook(template)

    assert template.exists()
    assert result.created_teachers == 1
    assert result.created_courses == 1
    assert result.created_subjects >= 3
    assert result.created_rooms == 1
    assert result.created_course_subjects >= 2
    assert result.updated_availability >= 2
    assert result.ok

    assignments = CourseSubjectService(database_path=db).list_assignments()
    assert len(assignments) >= 2

    teacher = TeacherService(database_path=db).list_teachers()[0]
    matrix = AvailabilityService(database_path=db).get_matrix(teacher.id)
    assert matrix[(1, 6)] == AvailabilityStatus.FORBIDDEN
