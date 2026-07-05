from pathlib import Path

from pini_desktop.services.course_service import Course, CourseService


def test_course_crud(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    service = CourseService(database_path=db)

    course_id = service.create_course(
        Course(
            id=None,
            code="1A",
            stage="Primaria",
            level=1,
            group_name="A",
            students=22,
            tutor_teacher_id=None,
        )
    )

    courses = service.list_courses()
    assert len(courses) == 1
    assert courses[0].id == course_id
    assert courses[0].code == "1A"

    service.update_course(
        Course(
            id=course_id,
            code="1A",
            stage="Primaria",
            level=1,
            group_name="A",
            students=24,
            tutor_teacher_id=None,
        )
    )

    assert service.list_courses()[0].students == 24

    service.delete_course(course_id)
    assert service.list_courses() == []
