from pathlib import Path

from pini_desktop.services.substitution_registry_service import SubstitutionRegistryService


def test_register_and_update_substitution(tmp_path: Path):
    db = tmp_path / "pini.db"
    service = SubstitutionRegistryService(database_path=db)

    record_id = service.register(
        absent_teacher_id=1,
        substitute_teacher_name="Luis Pérez",
        day=1,
        period=2,
        score=95,
        reasons="Libre; Guardia",
        warnings="",
    )

    records = service.list_records()
    assert len(records) == 1
    assert records[0].id == record_id
    assert records[0].status == "PLANNED"

    service.mark_done(record_id)
    assert service.list_records()[0].status == "DONE"

    service.cancel(record_id)
    assert service.list_records()[0].status == "CANCELLED"
