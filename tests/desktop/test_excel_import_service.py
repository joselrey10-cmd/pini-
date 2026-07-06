from pathlib import Path

from pini_desktop.services.excel_import_service import ExcelImportService


def test_excel_import_template_and_import(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    template = tmp_path / "plantilla.xlsx"

    service = ExcelImportService(database_path=db)
    service.create_template(template)
    result = service.import_workbook(template)

    assert template.exists()
    assert result.created_teachers == 1
    assert result.created_courses == 1
    assert result.created_subjects == 3
    assert result.created_rooms == 1
    assert result.ok
