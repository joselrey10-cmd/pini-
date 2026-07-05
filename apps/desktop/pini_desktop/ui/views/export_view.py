from pathlib import Path

from PySide6.QtWidgets import QComboBox, QFileDialog, QFormLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from pini_desktop.services.excel_export_service import ExcelExportService
from pini_desktop.services.pdf_export_service import PdfExportService
from pini_desktop.services.schedule_view_service import ScheduleViewService


class ExportView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.schedule_view_service = ScheduleViewService()
        self.excel_export_service = ExcelExportService()
        self.pdf_export_service = PdfExportService()

        self.course_combo = QComboBox()
        self.teacher_combo = QComboBox()

        reload_button = QPushButton("Actualizar listas")
        reload_button.clicked.connect(self.load_entities)

        export_course_excel_button = QPushButton("Exportar curso a Excel")
        export_course_excel_button.clicked.connect(self.export_course_excel)

        export_teacher_excel_button = QPushButton("Exportar profesor a Excel")
        export_teacher_excel_button.clicked.connect(self.export_teacher_excel)

        export_course_pdf_button = QPushButton("Exportar curso a PDF")
        export_course_pdf_button.clicked.connect(self.export_course_pdf)

        export_teacher_pdf_button = QPushButton("Exportar profesor a PDF")
        export_teacher_pdf_button.clicked.connect(self.export_teacher_pdf)

        form = QFormLayout()
        form.addRow("Curso", self.course_combo)
        form.addRow("Profesor/a", self.teacher_combo)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Exportación de horarios"))
        layout.addLayout(form)
        layout.addWidget(reload_button)
        layout.addWidget(export_course_excel_button)
        layout.addWidget(export_teacher_excel_button)
        layout.addWidget(export_course_pdf_button)
        layout.addWidget(export_teacher_pdf_button)
        layout.addStretch()

        self.load_entities()

    def load_entities(self) -> None:
        self.course_combo.clear()
        for course_id, label in self.schedule_view_service.list_courses():
            self.course_combo.addItem(label, course_id)

        self.teacher_combo.clear()
        for teacher_id, label in self.schedule_view_service.list_teachers():
            self.teacher_combo.addItem(label, teacher_id)

    def export_course_excel(self) -> None:
        self._export_course("xlsx", self.excel_export_service.export_course_schedule)

    def export_teacher_excel(self) -> None:
        self._export_teacher("xlsx", self.excel_export_service.export_teacher_schedule)

    def export_course_pdf(self) -> None:
        self._export_course("pdf", self.pdf_export_service.export_course_schedule)

    def export_teacher_pdf(self) -> None:
        self._export_teacher("pdf", self.pdf_export_service.export_teacher_schedule)

    def _export_course(self, extension: str, exporter) -> None:
        course_id = self.course_combo.currentData()
        if course_id is None:
            QMessageBox.information(self, "Sin cursos", "No hay cursos para exportar.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar horario del curso",
            str(Path.home() / f"horario_curso.{extension}"),
            f"{extension.upper()} (*.{extension})",
        )
        if path:
            exporter(course_id, path)
            QMessageBox.information(self, "Exportado", f"Horario exportado a:\n{path}")

    def _export_teacher(self, extension: str, exporter) -> None:
        teacher_id = self.teacher_combo.currentData()
        if teacher_id is None:
            QMessageBox.information(self, "Sin profesorado", "No hay profesorado para exportar.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar horario del profesor",
            str(Path.home() / f"horario_profesor.{extension}"),
            f"{extension.upper()} (*.{extension})",
        )
        if path:
            exporter(teacher_id, path)
            QMessageBox.information(self, "Exportado", f"Horario exportado a:\n{path}")
