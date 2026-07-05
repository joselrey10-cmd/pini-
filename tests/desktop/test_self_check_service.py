from pathlib import Path

from pini_desktop.services.self_check_service import SelfCheckService


def test_self_check_database_tables(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    service = SelfCheckService(database_path=db)

    items = service.run_checks()
    table_items = [item for item in items if item.area == "Base de datos"]

    assert table_items
    assert any(item.message.endswith("teachers") for item in table_items)
