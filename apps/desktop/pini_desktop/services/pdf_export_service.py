from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from pini_desktop.services.schedule_view_service import ScheduleViewService


class PdfExportService:
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
        path.parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(str(path), pagesize=landscape(A4))
        styles = getSampleStyleSheet()
        story = [Paragraph(title, styles["Title"]), Spacer(1, 12)]

        data = [["Periodo", *self.DAY_NAMES]]
        for period in range(1, 7):
            row = [f"P{period}"]
            for day in range(1, 6):
                cell = matrix.get((day, period))
                if not cell:
                    text = ""
                elif mode == "course":
                    text = "<br/>".join(part for part in [cell.subject_name, cell.teacher_name, cell.room_name] if part)
                else:
                    text = "<br/>".join(part for part in [cell.course_code, cell.subject_name, cell.room_name] if part)
                row.append(Paragraph(text, styles["BodyText"]))
            data.append(row)

        table = Table(data, colWidths=[60, 130, 130, 130, 130, 130])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
        ]))

        story.append(table)
        doc.build(story)
        return path

    def _find_label(self, items, entity_id: int) -> str:
        for item_id, label in items:
            if item_id == entity_id:
                return label
        return str(entity_id)
