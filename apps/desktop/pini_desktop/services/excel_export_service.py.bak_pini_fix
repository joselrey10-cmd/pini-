from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

from pini_desktop.services.schedule_view_service import ScheduleViewService


class ExcelExportService:
    DAY_NAMES = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    def __init__(self, database_path=None):
        self.schedule_view_service = ScheduleViewService(database_path) if database_path else ScheduleViewService()

    def export_course_schedule(self, course_id: int, path: str | Path) -> Path:
        matrix = self.schedule_view_service.course_matrix(course_id)
        label = self._find_label(self.schedule_view_service.list_courses(), course_id)
        return self._export_matrix(f"Horario curso {label}", path, matrix, "course")

    def export_teacher_schedule(self, teacher_id: int, path: str | Path) -> Path:
        matrix = self.schedule_view_service.teacher_matrix(teacher_id)
        label = self._find_label(self.schedule_view_service.list_teachers(), teacher_id)
        return self._export_matrix(f"Horario profesor/a {label}", path, matrix, "teacher")

    def _export_matrix(self, title: str, path: str | Path, matrix, mode: str) -> Path:
        path = Path(path)
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Horario"

        sheet["A1"] = title
        sheet["A1"].font = Font(bold=True, size=14)
        sheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=6)

        sheet.cell(row=3, column=1, value="Periodo").font = Font(bold=True)
        for index, day_name in enumerate(self.DAY_NAMES, start=2):
            cell = sheet.cell(row=3, column=index, value=day_name)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center")

        for period in range(1, 7):
            sheet.cell(row=period + 3, column=1, value=f"P{period}").font = Font(bold=True)
            for day in range(1, 6):
                schedule_cell = matrix.get((day, period))
                if not schedule_cell:
                    cell_value = ""
                elif mode == "course":
                    cell_value = "\n".join(part for part in [schedule_cell.subject_name, schedule_cell.teacher_name, schedule_cell.room_name] if part)
                else:
                    cell_value = "\n".join(part for part in [schedule_cell.course_code, schedule_cell.subject_name, schedule_cell.room_name] if part)

                cell = sheet.cell(row=period + 3, column=day + 1, value=cell_value)
                cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")

        for column in range(1, 7):
            sheet.column_dimensions[get_column_letter(column)].width = 24 if column > 1 else 12
        for row in range(4, 10):
            sheet.row_dimensions[row].height = 55

        path.parent.mkdir(parents=True, exist_ok=True)
        workbook.save(path)
        return path

    def _find_label(self, items, entity_id: int) -> str:
        for item_id, label in items:
            if item_id == entity_id:
                return label
        return str(entity_id)
