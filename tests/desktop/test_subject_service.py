from pathlib import Path

from pini_desktop.services.subject_service import Subject, SubjectService


def test_subject_crud(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    service = SubjectService(database_path=db)

    subject_id = service.create_subject(
        Subject(
            id=None,
            code="LEN",
            name="Lengua",
            weekly_sessions=5,
            required_speciality="Primaria",
            room_type="Ordinaria",
            max_consecutive=1,
            allows_double_session=False,
        )
    )

    subjects = service.list_subjects()
    assert len(subjects) == 1
    assert subjects[0].id == subject_id
    assert subjects[0].code == "LEN"

    service.update_subject(
        Subject(
            id=subject_id,
            code="LEN",
            name="Lengua Castellana",
            weekly_sessions=5,
            required_speciality="Primaria",
            room_type="Ordinaria",
            max_consecutive=1,
            allows_double_session=False,
        )
    )

    assert service.list_subjects()[0].name == "Lengua Castellana"

    service.delete_subject(subject_id)
    assert service.list_subjects() == []


def test_seed_default_subjects(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    service = SubjectService(database_path=db)
    service.seed_default_subjects()

    codes = {subject.code for subject in service.list_subjects()}
    assert "ING" in codes
    assert "CON" in codes
