from pathlib import Path

from pini_desktop.services.course_service import Course, CourseService
from pini_desktop.services.editor import EditorService
from pini_desktop.services.room_service import Room, RoomService
from pini_desktop.services.scheduler.domain import SchedulePlacement
from pini_desktop.services.scheduler.repository import SchedulerRepository
from pini_desktop.services.subject_service import Subject, SubjectService
from pini_desktop.services.teacher_service import Teacher, TeacherService
from pini_desktop.services.timetable_service import TimetableService, TimetableSettings


def build_editor_db(db: Path):
    teacher_service = TeacherService(database_path=db)
    course_service = CourseService(database_path=db)
    subject_service = SubjectService(database_path=db)
    room_service = RoomService(database_path=db)
    timetable_service = TimetableService(database_path=db)
    repository = SchedulerRepository(db)

    teacher_id = teacher_service.create_teacher(Teacher(None, "P01", "Ana", "García", "Primaria", 25, 5))
    other_teacher_id = teacher_service.create_teacher(Teacher(None, "P02", "Luis", "Pérez", "Primaria", 25, 5))
    course_id = course_service.create_course(Course(None, "1A", "Primaria", 1, "A", 22, teacher_id))
    other_course_id = course_service.create_course(Course(None, "2A", "Primaria", 2, "A", 20, other_teacher_id))
    subject_id = subject_service.create_subject(Subject(None, "LEN", "Lengua", 2, "Primaria", "Ordinaria", 1, False))
    other_subject_id = subject_service.create_subject(Subject(None, "MAT", "Mate", 2, "Primaria", "Ordinaria", 1, False))
    room_id = room_service.create_room(Room(None, "A1", "Aula 1", "Ordinaria", 25, "", "", True))
    other_room_id = room_service.create_room(Room(None, "A2", "Aula 2", "Ordinaria", 25, "", "", True))
    timetable_service.save_settings(TimetableSettings())
    timetable_service.save_generated_periods()
    repository.save_placements([
        SchedulePlacement(course_id, subject_id, teacher_id, room_id, 1, 1, "test"),
        SchedulePlacement(other_course_id, other_subject_id, other_teacher_id, other_room_id, 1, 2, "test"),
    ])
    return EditorService(database_path=db)


def test_editor_service_moves_session_and_undo_redo(tmp_path: Path):
    db = tmp_path / "pini.db"
    service = build_editor_db(db)
    session = service.list_sessions()[0]

    result = service.move_session(session.id, 2, 3)
    assert result.success

    moved = next(item for item in service.list_sessions() if item.id == session.id)
    assert (moved.day, moved.period) == (2, 3)

    undo = service.undo()
    assert undo.success
    restored = next(item for item in service.list_sessions() if item.id == session.id)
    assert (restored.day, restored.period) == (1, 1)

    redo = service.redo()
    assert redo.success
    moved_again = next(item for item in service.list_sessions() if item.id == session.id)
    assert (moved_again.day, moved_again.period) == (2, 3)


def test_editor_service_rejects_teacher_conflict(tmp_path: Path):
    db = tmp_path / "pini.db"
    service = build_editor_db(db)
    sessions = service.list_sessions()
    first = sessions[0]
    second = sessions[1]

    # Force same teacher to create a real teacher conflict at target.
    import sqlite3
    con = sqlite3.connect(db)
    con.execute("UPDATE schedule_sessions SET teacher_id=? WHERE id=?", (first.teacher_id, second.id))
    con.commit()
    con.close()

    result = service.move_session(first.id, second.day, second.period)
    assert not result.success
    assert any("profesor" in warning.lower() for warning in result.warnings)


def test_editor_service_swaps_sessions(tmp_path: Path):
    db = tmp_path / "pini.db"
    service = build_editor_db(db)
    first, second = service.list_sessions()[:2]

    result = service.swap_sessions(first.id, second.id)
    assert result.success

    sessions = {item.id: item for item in service.list_sessions()}
    assert (sessions[first.id].day, sessions[first.id].period) == (second.day, second.period)
    assert (sessions[second.id].day, sessions[second.id].period) == (first.day, first.period)
