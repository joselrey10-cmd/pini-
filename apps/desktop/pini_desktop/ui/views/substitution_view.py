from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from pini_desktop.services.substitution_service import PiniSubstitutionService
from pini_desktop.services.teacher_service import TeacherService


class SubstitutionView(QWidget):
    HEADERS = ["Profesor/a", "Puntuación", "Motivos", "Avisos"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.teacher_service = TeacherService()
        self.substitution_service = PiniSubstitutionService()

        title = QLabel("Sustituciones inteligentes")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        description = QLabel(
            "Selecciona el profesor ausente, día y periodo. Pini propondrá las mejores sustituciones disponibles."
        )
        description.setWordWrap(True)

        self.teacher_combo = QComboBox()
        self.day_input = QSpinBox()
        self.day_input.setRange(1, 5)
        self.day_input.setValue(1)

        self.period_input = QSpinBox()
        self.period_input.setRange(1, 8)
        self.period_input.setValue(1)

        form = QFormLayout()
        form.addRow("Profesor ausente", self.teacher_combo)
        form.addRow("Día", self.day_input)
        form.addRow("Periodo", self.period_input)

        find_button = QPushButton("Buscar sustituciones")
        find_button.clicked.connect(self.find_substitutions)

        refresh_button = QPushButton("Actualizar profesorado")
        refresh_button.clicked.connect(self.load_teachers)

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addLayout(form)
        layout.addWidget(find_button)
        layout.addWidget(refresh_button)
        layout.addWidget(self.table)

        self.load_teachers()

    def load_teachers(self) -> None:
        self.teacher_combo.clear()
        for teacher in self.teacher_service.list_teachers():
            label = f"{teacher.name} {teacher.surname}"
            self.teacher_combo.addItem(label, teacher.id)

    def find_substitutions(self) -> None:
        teacher_id = self.teacher_combo.currentData()
        if teacher_id is None:
            QMessageBox.information(self, "Sin profesorado", "No hay profesorado cargado.")
            return

        proposals = self.substitution_service.propose_for_absence(
            absent_teacher_id=int(teacher_id),
            day=self.day_input.value(),
            period=self.period_input.value(),
        )

        self.table.setRowCount(len(proposals))

        for row_index, proposal in enumerate(proposals):
            values = [
                proposal.teacher,
                str(proposal.score),
                "; ".join(proposal.reasons),
                "; ".join(proposal.warnings),
            ]
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column_index == 1:
                    item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, column_index, item)

        self.table.resizeColumnsToContents()

        if not proposals:
            QMessageBox.information(
                self,
                "Sin propuestas",
                "No se han encontrado sustituciones disponibles para esa franja.",
            )
