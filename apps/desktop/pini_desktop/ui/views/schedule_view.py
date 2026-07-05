from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)

from pini_desktop.services.scheduler_service import SchedulerService


class ScheduleView(QWidget):
    HEADERS = ["Día", "Periodo", "Curso", "Materia", "Profesor/a", "Aula"]

    DAY_NAMES = {
        1: "Lunes",
        2: "Martes",
        3: "Miércoles",
        4: "Jueves",
        5: "Viernes",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = SchedulerService()

        generate_button = QPushButton("Generar horario básico")
        generate_button.clicked.connect(self.generate_schedule)

        clear_button = QPushButton("Limpiar horario generado")
        clear_button.clicked.connect(self.clear_schedule)

        refresh_button = QPushButton("Actualizar")
        refresh_button.clicked.connect(self.load_sessions)

        buttons = QHBoxLayout()
        buttons.addWidget(generate_button)
        buttons.addWidget(clear_button)
        buttons.addStretch()
        buttons.addWidget(refresh_button)

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        layout = QVBoxLayout(self)
        layout.addLayout(buttons)
        layout.addWidget(self.table)

        self.load_sessions()

    def generate_schedule(self) -> None:
        warnings = self.service.generate_basic_schedule()
        self.load_sessions()

        if warnings:
            QMessageBox.warning(self, "Horario generado con avisos", "\n".join(warnings[:10]))
        else:
            QMessageBox.information(self, "Horario generado", "Horario básico generado correctamente.")

    def clear_schedule(self) -> None:
        self.service.clear_generated_schedule()
        self.load_sessions()

    def load_sessions(self) -> None:
        sessions = self.service.list_sessions()
        self.table.setRowCount(len(sessions))

        for row_index, session in enumerate(sessions):
            values = [
                self.DAY_NAMES.get(session.day, str(session.day)),
                f"P{session.period}",
                session.course_code,
                session.subject_name,
                session.teacher_name,
                session.room_name,
            ]
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, column_index, item)

        self.table.resizeColumnsToContents()
