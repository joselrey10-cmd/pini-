from pathlib import Path

from pini_desktop.services.course_service import Course, CourseService
from pini_desktop.services.course_subject_service import CourseSubject, CourseSubjectService
from pini_desktop.services.project_validation_service import ProjectValidationService, ValidationSeverity
from pini_desktop.services.room_service import Room, RoomService
from pini_desktop.services.subject_service import Subject, SubjectService
from pini_desktop.services.teacher_service import Teacher, TeacherService
from pini_desktop.services.timetable_service import TimetableService, TimetableSettings


def test_empty_project_has_errors(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    service = ProjectValidationService(database_path=db)

    issues = service.validate()

    assert any(issue.severity == ValidationSeverity.ERROR for issue in issues)


def test_complete_minimal_project_has_no_blocking_errors(tmp_path: Path):
    db = tmp_path / "test_pini.db"

    teacher_service = TeacherService(database_path=db)
    course_service = CourseService(database_path=db)
    subject_service = SubjectService(database_path=db)
    room_service = RoomService(database_path=db)
    assignment_service = CourseSubjectService(database_path=db)
    timetable_service = TimetableService(database_path=db)

    teacher_id = teacher_service.create_teacher(
        Teacher(None, "P01", "Ana", "García", "Primaria", 25, 5)
    )
    course_id = course_service.create_course(
        Course(None, "1A", "Primaria", 1, "A", 22, teacher_id)
    )
    subject_id = subject_service.create_subject(
        Subject(None, "LEN", "Lengua", 5, "Primaria", "Ordinaria", 1, False)
    )
    room_service.create_room(
        Room(None, "A1", "Aula 1", "Ordinaria", 25, "Principal", "", True)
    )
    assignment_service.create_assignment(
        CourseSubject(None, course_id, subject_id, 5, teacher_id, "Ordinaria", "")
    )
    timetable_service.save_settings(TimetableSettings())
    timetable_service.save_generated_periods()

    validation_service = ProjectValidationService(database_path=db)
    issues = validation_service.validate()

    assert not any(issue.severity == ValidationSeverity.ERROR for issue in issues)
