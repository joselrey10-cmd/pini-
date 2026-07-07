from pathlib import Path

from pini_desktop.services.editor.history.editor_history_service import EditorHistoryService


class DummyResult:
    success = True
    messages = ("Movimiento aplicado",)
    warnings = ()
    old_score = 80
    new_score = 85


def test_editor_history_service_records_result(tmp_path: Path):
    service = EditorHistoryService(database_path=tmp_path / "pini.db")

    record_id = service.record_result("Mover sesión", DummyResult())
    records = service.list_records()

    assert record_id > 0
    assert len(records) == 1
    assert records[0].action == "Mover sesión"
    assert records[0].success
    assert records[0].old_score == 80
    assert records[0].new_score == 85


def test_editor_history_service_clear(tmp_path: Path):
    service = EditorHistoryService(database_path=tmp_path / "pini.db")
    service.record_result("Mover sesión", DummyResult())

    service.clear()

    assert service.list_records() == []
