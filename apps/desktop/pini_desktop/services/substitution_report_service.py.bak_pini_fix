from dataclasses import dataclass
from pathlib import Path
from openpyxl import Workbook

from pini_desktop.config.settings import DATA_DIR
from pini_desktop.services.substitution_registry_service import SubstitutionRegistryService


@dataclass(frozen=True)
class SubstitutionReportSummary:
    total: int
    planned: int
    done: int
    cancelled: int


class SubstitutionReportService:
    def __init__(self, database_path=None):
        self.registry = SubstitutionRegistryService(database_path) if database_path else SubstitutionRegistryService()

    def summary(self) -> SubstitutionReportSummary:
        records = self.registry.list_records()
        return SubstitutionReportSummary(
            total=len(records),
            planned=sum(1 for r in records if r.status == "PLANNED"),
            done=sum(1 for r in records if r.status == "DONE"),
            cancelled=sum(1 for r in records if r.status == "CANCELLED"),
        )

    def export_excel(self, destination: str | Path | None = None) -> Path:
        records = self.registry.list_records()

        if destination is None:
            export_dir = DATA_DIR / "exports"
            export_dir.mkdir(parents=True, exist_ok=True)
            destination = export_dir / "sustituciones.xlsx"

        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)

        wb = Workbook()
        ws = wb.active
        ws.title = "Sustituciones"
        ws.append([
            "ID",
            "Ausente ID",
            "Sustituto/a",
            "Día",
            "Periodo",
            "Puntuación",
            "Estado",
            "Motivos",
            "Avisos",
            "Creado",
        ])

        for r in records:
            ws.append([
                r.id,
                r.absent_teacher_id,
                r.substitute_teacher_name,
                r.day,
                r.period,
                r.score,
                r.status,
                r.reasons,
                r.warnings,
                r.created_at,
            ])

        for column in ws.columns:
            max_length = 0
            letter = column[0].column_letter
            for cell in column:
                value = str(cell.value or "")
                max_length = max(max_length, len(value))
            ws.column_dimensions[letter].width = min(max_length + 2, 50)

        wb.save(destination)
        return destination
