from pathlib import Path

from PySide6.QtWidgets import QComboBox, QFileDialog, QFormLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from pini_desktop.services.excel_export_service import ExcelExportService
from pini_desktop.services.schedule_view_service import ScheduleViewService


class ExportView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.schedule_view_service = ScheduleViewService()
        self.export_service = ExcelExportService()

        self.course_combo = QComboBox()
        self.teacher_combo = QComboBox()

        reload_button = QPushButton("Actualizar listas")
        reload_button.clicked.connect(self.load_entities)

        export_course_button = QPushButton("Exportar horario por curso a Excel")
        export_course_button.clicked.connect(self.export_course)

        export_teacher_button = QPushButton("Exportar horario por profesor a Excel")
        export_teacher_button.clicked.connect(self.export_teacher)

        form = QFormLayout()
        form.addRow("Curso", self.course_combo)
        form.addRow("Profesor/a", self.teacher_combo)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Exportación a Excel"))
        layout.addLayout(form)
        layout.addWidget(reload_button)
        layout.addWidget(export_course_button)
        layout.addWidget(export_teacher_button)
        layout.addStretch()

        self.load_entities()

    def load_entities(self) -> None:
        self.course_combo.clear()
        for course_id, label in self.schedule_view_service.list_courses():
            self.course_combo.addItem(label, course_id)

        self.teacher_combo.clear()
        for teacher_id, label in self.schedule_view_service.list_teachers():
            self.teacher_combo.addItem(label, teacher_id)

    def export_course(self) -> None:
        course_id = self.course_combo.currentData()
        if course_id is None:
            QMessageBox.information(self, "Sin cursos", "No hay cursos para exportar.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Guardar horario del curso", str(Path.home() / "horario_curso.xlsx"), "Excel (*.xlsx)")
        if path:
            self.export_service.export_course_schedule(course_id, path)
            QMessageBox.information(self, "Exportado", f"Horario exportado a:\n{path}")

    def export_teacher(self) -> None:
        teacher_id = self.teacher_combo.currentData()
        if teacher_id is None:
            QMessageBox.information(self, "Sin profesorado", "No hay profesorado para exportar.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Guardar horario del profesor", str(Path.home() / "horario_profesor.xlsx"), "Excel (*.xlsx)")
        if path:
            self.export_service.export_teacher_schedule(teacher_id, path)
            QMessageBox.information(self, "Exportado", f"Horario exportado a:\n{path}")
