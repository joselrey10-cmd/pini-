from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from pini_desktop.services.excel_import_service import ExcelImportService


class ImportView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = ExcelImportService()

        title = QLabel("Importación desde Excel")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        description = QLabel(
            "Permite crear una plantilla Excel e importar profesores, cursos, materias, aulas, materias por curso y disponibilidad."
        )
        description.setWordWrap(True)

        template_button = QPushButton("Crear plantilla Excel completa")
        template_button.clicked.connect(self.create_template)

        import_button = QPushButton("Importar datos desde Excel")
        import_button.clicked.connect(self.import_excel)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(template_button)
        layout.addWidget(import_button)
        layout.addStretch()

    def create_template(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar plantilla",
            str(Path.home() / "plantilla_pini_completa.xlsx"),
            "Excel (*.xlsx)",
        )
        if path:
            self.service.create_template(path)
            QMessageBox.information(self, "Plantilla creada", f"Plantilla guardada en:\\n{path}")

    def import_excel(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Excel",
            str(Path.home()),
            "Excel (*.xlsx)",
        )
        if not path:
            return

        result = self.service.import_workbook(path)
        message = (
            f"Profesores creados: {result.created_teachers}\\n"
            f"Cursos creados: {result.created_courses}\\n"
            f"Materias creadas: {result.created_subjects}\\n"
            f"Aulas creadas: {result.created_rooms}\\n"
            f"Materias por curso creadas: {result.created_course_subjects}\\n"
            f"Disponibilidades actualizadas: {result.updated_availability}"
        )

        if result.errors:
            message += "\\n\\nErrores:\\n" + "\\n".join(result.errors[:12])
            QMessageBox.warning(self, "Importación con avisos", message)
        else:
            QMessageBox.information(self, "Importación completada", message)
