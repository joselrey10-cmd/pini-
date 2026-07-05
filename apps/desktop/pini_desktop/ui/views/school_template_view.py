from PySide6.QtWidgets import QCheckBox, QGroupBox, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from pini_desktop.services.school_template_service import SchoolTemplateService


class SchoolTemplateView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = SchoolTemplateService()

        title = QLabel("Plantillas automáticas del colegio")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        description = QLabel(
            "Crea datos base: cursos de Primaria, materias, aulas y reglas. No borra datos existentes."
        )
        description.setWordWrap(True)

        group_box = QGroupBox("Líneas del centro")
        group_layout = QVBoxLayout(group_box)

        self.group_a = QCheckBox("Línea A")
        self.group_a.setChecked(True)
        self.group_b = QCheckBox("Línea B")
        self.group_c = QCheckBox("Línea C")

        group_layout.addWidget(self.group_a)
        group_layout.addWidget(self.group_b)
        group_layout.addWidget(self.group_c)

        create_button = QPushButton("Crear plantilla CEIP Primaria")
        create_button.clicked.connect(self.create_primary_template)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(group_box)
        layout.addWidget(create_button)
        layout.addStretch()

    def selected_groups(self) -> list[str]:
        groups = []
        if self.group_a.isChecked():
            groups.append("A")
        if self.group_b.isChecked():
            groups.append("B")
        if self.group_c.isChecked():
            groups.append("C")
        return groups or ["A"]

    def create_primary_template(self) -> None:
        result = self.service.create_primary_template(self.selected_groups())
        QMessageBox.information(
            self,
            "Plantilla creada",
            (
                f"Cursos creados: {result.created_courses}\n"
                f"Materias creadas: {result.created_subjects}\n"
                f"Aulas creadas: {result.created_rooms}\n"
                f"Reglas creadas: {result.created_rules}"
            ),
        )
