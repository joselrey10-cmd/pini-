from pathlib import Path

from pini_desktop.services.dynamic_rule_service import DynamicRuleService
from pini_desktop.services.excel_import_service import ExcelImportService


def test_excel_import_includes_dynamic_rules(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    template = tmp_path / "plantilla_completa.xlsx"

    service = ExcelImportService(database_path=db)
    service.create_template(template)
    result = service.import_workbook(template)

    assert result.created_dynamic_rules >= 3
    assert result.ok

    rules = DynamicRuleService(database_path=db).list_rules()
    codes = {rule.code for rule in rules}
    assert {"R001", "R002", "R003"} <= codes
