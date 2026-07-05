from pathlib import Path

from pini_desktop.services.availability_service import AvailabilityService, AvailabilityStatus
from pini_desktop.services.teacher_service import Teacher, TeacherService


def test_teacher_availability_matrix(tmp_path: Path):
    db = tmp_path / "test_pini.db"

    teacher_service = TeacherService(database_path=db)
    teacher_id = teacher_service.create_teacher(
        Teacher(None, "P01", "Ana", "García", "Primaria", 25, 5)
    )

    availability_service = AvailabilityService(database_path=db)
    matrix = availability_service.get_matrix(teacher_id)

    assert len(matrix) == 30
    assert matrix[(1, 1)] == AvailabilityStatus.AVAILABLE

    availability_service.set_status(teacher_id, 2, 3, AvailabilityStatus.FORBIDDEN)
    matrix = availability_service.get_matrix(teacher_id)

    assert matrix[(2, 3)] == AvailabilityStatus.FORBIDDEN
