from pathlib import Path

from pini_desktop.services.course_service import Course, CourseService
from pini_desktop.services.course_subject_service import CourseSubject, CourseSubjectService
from pini_desktop.services.room_service import Room, RoomService
from pini_desktop.services.scheduler_service import SchedulerService
from pini_desktop.services.subject_service import Subject, SubjectService
from pini_desktop.services.teacher_service import Teacher, TeacherService
from pini_desktop.services.timetable_service import TimetableService, TimetableSettings


def test_ortools_scheduler_generates_sessions(tmp_path: Path):
    db = tmp_path / "test_pini.db"

    teacher_service = TeacherService(database_path=db)
    course_service = CourseService(database_path=db)
    subject_service = SubjectService(database_path=db)
    room_service = RoomService(database_path=db)
    assignment_service = CourseSubjectService(database_path=db)
    timetable_service = TimetableService(database_path=db)
    scheduler_service = SchedulerService(database_path=db)

    teacher_id = teacher_service.create_teacher(Teacher(None, "P01", "Ana", "García", "Primaria", 25, 5))
    course_id = course_service.create_course(Course(None, "1A", "Primaria", 1, "A", 22, teacher_id))
    subject_id = subject_service.create_subject(Subject(None, "LEN", "Lengua", 2, "Primaria", "Ordinaria", 1, False))
    room_service.create_room(Room(None, "A1", "Aula 1", "Ordinaria", 25, "Principal", "", True))
    assignment_service.create_assignment(CourseSubject(None, course_id, subject_id, 2, teacher_id, "Ordinaria", ""))
    timetable_service.save_settings(TimetableSettings())
    timetable_service.save_generated_periods()

    warnings = scheduler_service.generate_ortools_schedule()
    sessions = scheduler_service.list_sessions()

    assert warnings == []
    assert len(sessions) == 2
