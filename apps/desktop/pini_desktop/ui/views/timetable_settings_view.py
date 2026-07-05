from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import QTime

from pini_desktop.services.timetable_service import TimetableService, TimetableSettings


class TimetableSettingsView(QWidget):
    DAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = TimetableService()

        settings = self.service.get_settings()

        self.working_days_input = QSpinBox()
        self.working_days_input.setRange(1, 5)
        self.working_days_input.setValue(settings.working_days)

        self.sessions_input = QSpinBox()
        self.sessions_input.setRange(1, 8)
        self.sessions_input.setValue(settings.sessions_per_day)

        self.duration_input = QSpinBox()
        self.duration_input.setRange(30, 90)
        self.duration_input.setValue(settings.session_duration_minutes)

        self.break_after_input = QSpinBox()
        self.break_after_input.setRange(1, 8)
        self.break_after_input.setValue(settings.break_after_period)

        self.break_duration_input = QSpinBox()
        self.break_duration_input.setRange(0, 60)
        self.break_duration_input.setValue(settings.break_duration_minutes)

        self.start_time_input = QTimeEdit()
        hour, minute = [int(part) for part in settings.start_time.split(":")]
        self.start_time_input.setTime(QTime(hour, minute))
        self.start_time_input.setDisplayFormat("HH:mm")

        form = QFormLayout()
        form.addRow("Días lectivos", self.working_days_input)
        form.addRow("Sesiones por día", self.sessions_input)
        form.addRow("Duración sesión (min)", self.duration_input)
        form.addRow("Recreo después de P", self.break_after_input)
        form.addRow("Duración recreo (min)", self.break_duration_input)
        form.addRow("Hora de inicio", self.start_time_input)

        save_button = QPushButton("Guardar configuración")
        save_button.clicked.connect(self.save_settings)

        generate_button = QPushButton("Generar periodos")
        generate_button.clicked.connect(self.generate_periods)

        buttons = QHBoxLayout()
        buttons.addWidget(save_button)
        buttons.addWidget(generate_button)
        buttons.addStretch()

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Día", "Periodo", "Inicio", "Fin", "Recreo después", "Después recreo"])

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Horario general del centro"))
        layout.addLayout(form)
        layout.addLayout(buttons)
        layout.addWidget(self.table)

        self.load_periods()

    def current_settings(self) -> TimetableSettings:
        return TimetableSettings(
            working_days=self.working_days_input.value(),
            sessions_per_day=self.sessions_input.value(),
            session_duration_minutes=self.duration_input.value(),
            break_after_period=self.break_after_input.value(),
            break_duration_minutes=self.break_duration_input.value(),
            start_time=self.start_time_input.time().toString("HH:mm"),
        )

    def save_settings(self) -> None:
        settings = self.current_settings()
        if settings.break_after_period >= settings.sessions_per_day:
            QMessageBox.warning(self, "Configuración incorrecta", "El recreo debe estar antes de la última sesión.")
            return
        self.service.save_settings(settings)
        QMessageBox.information(self, "Guardado", "Configuración horaria guardada.")

    def generate_periods(self) -> None:
        settings = self.current_settings()
        if settings.break_after_period >= settings.sessions_per_day:
            QMessageBox.warning(self, "Configuración incorrecta", "El recreo debe estar antes de la última sesión.")
            return
        self.service.save_settings(settings)
        self.service.save_generated_periods(settings)
        self.load_periods()
        QMessageBox.information(self, "Periodos generados", "Se han generado los periodos del horario.")

    def load_periods(self) -> None:
        periods = self.service.list_periods()
        if not periods:
            periods = self.service.generate_periods(self.service.get_settings())

        self.table.setRowCount(len(periods))
        for row_index, period in enumerate(periods):
            day_name = self.DAYS[period.day - 1] if 1 <= period.day <= len(self.DAYS) else str(period.day)
            values = [
                day_name,
                f"P{period.period}",
                period.start_time,
                period.end_time,
                "Sí" if period.is_break_after else "No",
                "Sí" if period.is_after_break else "No",
            ]
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, column_index, item)

        self.table.resizeColumnsToContents()
