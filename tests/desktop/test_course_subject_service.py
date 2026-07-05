from pathlib import Path

from pini_desktop.services.course_service import Course, CourseService
from pini_desktop.services.course_subject_service import CourseSubject, CourseSubjectService
from pini_desktop.services.subject_service import Subject, SubjectService
from pini_desktop.services.teacher_service import Teacher, TeacherService


def test_course_subject_crud(tmp_path: Path):
    db = tmp_path / "test_pini.db"

    teacher_service = TeacherService(database_path=db)
    course_service = CourseService(database_path=db)
    subject_service = SubjectService(database_path=db)
    assignment_service = CourseSubjectService(database_path=db)

    teacher_id = teacher_service.create_teacher(
        Teacher(None, "P01", "Ana", "García", "Primaria", 25, 5)
    )
    course_id = course_service.create_course(
        Course(None, "1A", "Primaria", 1, "A", 22, teacher_id)
    )
    subject_id = subject_service.create_subject(
        Subject(None, "LEN", "Lengua", 5, "Primaria", "Ordinaria", 1, False)
    )

    assignment_id = assignment_service.create_assignment(
        CourseSubject(
            id=None,
            course_id=course_id,
            subject_id=subject_id,
            weekly_sessions=5,
            preferred_teacher_id=teacher_id,
            required_room_type="Ordinaria",
            notes="Tutoría",
        )
    )

    assignments = assignment_service.list_assignments()
    assert len(assignments) == 1
    assert assignments[0].id == assignment_id
    assert assignments[0].course_code == "1A"
    assert assignments[0].subject_name == "Lengua"

    assignment_service.update_assignment(
        CourseSubject(
            id=assignment_id,
            course_id=course_id,
            subject_id=subject_id,
            weekly_sessions=4,
            preferred_teacher_id=teacher_id,
            required_room_type="Ordinaria",
            notes="Ajustado",
        )
    )

    assert assignment_service.list_assignments()[0].weekly_sessions == 4

    assignment_service.delete_assignment(assignment_id)
    assert assignment_service.list_assignments() == []
