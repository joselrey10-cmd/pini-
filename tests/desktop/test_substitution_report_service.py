from pathlib import Path

from pini_desktop.services.substitution_registry_service import SubstitutionRegistryService
from pini_desktop.services.substitution_report_service import SubstitutionReportService


def test_substitution_report_summary_and_export(tmp_path: Path):
    db = tmp_path / "pini.db"
    output = tmp_path / "sustituciones.xlsx"

    registry = SubstitutionRegistryService(database_path=db)
    record_id = registry.register(1, "Luis Pérez", 1, 2, 95, "Libre", "")
    registry.mark_done(record_id)

    service = SubstitutionReportService(database_path=db)
    summary = service.summary()

    assert summary.total == 1
    assert summary.done == 1

    exported = service.export_excel(output)
    assert exported.exists()
