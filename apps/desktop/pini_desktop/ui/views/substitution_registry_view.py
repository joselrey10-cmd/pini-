from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from pini_desktop.services.substitution_registry_service import SubstitutionRegistryService


class SubstitutionRegistryView(QWidget):
    HEADERS = ["ID", "Ausente ID", "Sustituto/a", "Día", "Periodo", "Puntuación", "Estado", "Motivos", "Avisos"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = SubstitutionRegistryService()

        title = QLabel("Registro de sustituciones")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        description = QLabel("Consulta las sustituciones planificadas, realizadas o canceladas.")
        description.setWordWrap(True)

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        refresh_button = QPushButton("Actualizar")
        refresh_button.clicked.connect(self.load_records)

        done_button = QPushButton("Marcar como realizada")
        done_button.clicked.connect(self.mark_selected_done)

        cancel_button = QPushButton("Cancelar sustitución")
        cancel_button.clicked.connect(self.cancel_selected)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(refresh_button)
        layout.addWidget(done_button)
        layout.addWidget(cancel_button)
        layout.addWidget(self.table)

        self.load_records()

    def load_records(self):
        records = self.service.list_records()
        self.table.setRowCount(len(records))

        for row_index, record in enumerate(records):
            values = [
                record.id,
                record.absent_teacher_id,
                record.substitute_teacher_name,
                record.day,
                record.period,
                record.score,
                record.status,
                record.reasons,
                record.warnings,
            ]
            for col_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                if col_index in (0, 1, 3, 4, 5, 6):
                    item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, col_index, item)

        self.table.resizeColumnsToContents()

    def selected_record_id(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            QMessageBox.information(self, "Selecciona una sustitución", "Selecciona una fila del registro.")
            return None
        return int(self.table.item(rows[0].row(), 0).text())

    def mark_selected_done(self):
        record_id = self.selected_record_id()
        if record_id is None:
            return
        self.service.mark_done(record_id)
        self.load_records()

    def cancel_selected(self):
        record_id = self.selected_record_id()
        if record_id is None:
            return
        self.service.cancel(record_id)
        self.load_records()
