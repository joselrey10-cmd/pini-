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

from pini_desktop.services.substitution_registry_service import SubstitutionRegistryService
from pini_desktop.services.substitution_service import PiniSubstitutionService
from pini_desktop.services.teacher_service import TeacherService


class SubstitutionView(QWidget):
    HEADERS = ["Periodo", "Profesor/a", "Puntuación", "Motivos", "Avisos"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.teacher_service = TeacherService()
        self.substitution_service = PiniSubstitutionService()
        self.registry_service = SubstitutionRegistryService()
        self.current_rows = []

        title = QLabel("Sustituciones inteligentes")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        description = QLabel(
            "Selecciona el profesor ausente, el día y el tramo horario. "
            "Pini propondrá sustituciones para cada periodo. Después puedes guardar la propuesta seleccionada."
        )
        description.setWordWrap(True)

        self.teacher_combo = QComboBox()

        self.day_input = QSpinBox()
        self.day_input.setRange(1, 5)
        self.day_input.setValue(1)

        self.start_period_input = QSpinBox()
        self.start_period_input.setRange(1, 8)
        self.start_period_input.setValue(1)

        self.end_period_input = QSpinBox()
        self.end_period_input.setRange(1, 8)
        self.end_period_input.setValue(1)

        form = QFormLayout()
        form.addRow("Profesor ausente", self.teacher_combo)
        form.addRow("Día", self.day_input)
        form.addRow("Desde periodo", self.start_period_input)
        form.addRow("Hasta periodo", self.end_period_input)

        find_button = QPushButton("Buscar sustituciones")
        find_button.clicked.connect(self.find_substitutions)

        register_button = QPushButton("Guardar propuesta seleccionada")
        register_button.clicked.connect(self.register_selected_proposal)

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
        layout.addWidget(register_button)
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

        start_period = self.start_period_input.value()
        end_period = self.end_period_input.value()

        if end_period < start_period:
            QMessageBox.warning(self, "Tramo incorrecto", "El periodo final no puede ser menor que el inicial.")
            return

        plans = self.substitution_service.propose_for_absence_range(
            absent_teacher_id=int(teacher_id),
            day=self.day_input.value(),
            start_period=start_period,
            end_period=end_period,
        )

        self.current_rows = []
        for plan in plans:
            if plan.proposals:
                for proposal in plan.proposals:
                    self.current_rows.append((plan.period, proposal))
            else:
                self.current_rows.append((plan.period, None))

        self.table.setRowCount(len(self.current_rows))

        for row_index, (period, proposal) in enumerate(self.current_rows):
            if proposal is None:
                values = [f"P{period}", "Sin propuesta", "", "", "No hay candidatos disponibles"]
            else:
                values = [
                    f"P{period}",
                    proposal.teacher,
                    str(proposal.score),
                    "; ".join(proposal.reasons),
                    "; ".join(proposal.warnings),
                ]

            for column_index, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column_index in (0, 2):
                    item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, column_index, item)

        self.table.resizeColumnsToContents()

        if not self.current_rows:
            QMessageBox.information(
                self,
                "Sin propuestas",
                "No se han encontrado sustituciones disponibles para ese tramo.",
            )

    def register_selected_proposal(self) -> None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            QMessageBox.information(self, "Selecciona propuesta", "Selecciona una propuesta de la tabla.")
            return

        row = selected[0].row()
        if row >= len(self.current_rows):
            return

        period, proposal = self.current_rows[row]
        if proposal is None:
            QMessageBox.warning(self, "Sin propuesta", "No se puede guardar un periodo sin propuesta.")
            return

        teacher_id = self.teacher_combo.currentData()
        if teacher_id is None:
            QMessageBox.warning(self, "Sin profesor", "No hay profesor ausente seleccionado.")
            return

        record_id = self.registry_service.register(
            absent_teacher_id=int(teacher_id),
            substitute_teacher_name=proposal.teacher,
            day=self.day_input.value(),
            period=period,
            score=proposal.score,
            reasons="; ".join(proposal.reasons),
            warnings="; ".join(proposal.warnings),
        )

        QMessageBox.information(
            self,
            "Sustitución guardada",
            f"Sustitución registrada correctamente con ID {record_id}.",
        )
