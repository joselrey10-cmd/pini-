from PySide6.QtCore import QTime
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QStackedWidget,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

from pini_desktop.services.center_config_service import CenterConfig, CenterConfigService
from pini_desktop.services.timetable_service import TimetableService, TimetableSettings


class CenterWizardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_service = CenterConfigService()
        self.timetable_service = TimetableService()

        self.current_config = self.config_service.get_config()

        self.stack = QStackedWidget()
        self.stack.addWidget(self._page_center_data())
        self.stack.addWidget(self._page_center_type())
        self.stack.addWidget(self._page_timetable())
        self.stack.addWidget(self._page_finish())

        self.back_button = QPushButton("Atrás")
        self.back_button.clicked.connect(self.previous_page)

        self.next_button = QPushButton("Siguiente")
        self.next_button.clicked.connect(self.next_page)

        self.finish_button = QPushButton("Guardar configuración")
        self.finish_button.clicked.connect(self.finish_wizard)

        buttons = QHBoxLayout()
        buttons.addWidget(self.back_button)
        buttons.addStretch()
        buttons.addWidget(self.next_button)
        buttons.addWidget(self.finish_button)

        layout = QVBoxLayout(self)
        title = QLabel("Asistente de configuración del centro")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        layout.addWidget(self.stack)
        layout.addLayout(buttons)

        self._refresh_buttons()

    def _page_center_data(self) -> QWidget:
        page = QWidget()
        layout = QFormLayout(page)

        self.center_name_input = QLineEdit(self.current_config.center_name)
        self.center_code_input = QLineEdit(self.current_config.center_code)
        self.locality_input = QLineEdit(self.current_config.locality)
        self.province_input = QLineEdit(self.current_config.province)
        self.school_year_input = QLineEdit(self.current_config.school_year)

        layout.addRow("Nombre del centro", self.center_name_input)
        layout.addRow("Código de centro", self.center_code_input)
        layout.addRow("Localidad", self.locality_input)
        layout.addRow("Provincia", self.province_input)
        layout.addRow("Curso escolar", self.school_year_input)
        return page

    def _page_center_type(self) -> QWidget:
        page = QWidget()
        layout = QFormLayout(page)

        self.center_type_input = QComboBox()
        self.center_type_input.addItems(["CEIP", "CRA", "CEO", "Infantil", "Primaria", "Secundaria"])
        self._select_text(self.center_type_input, self.current_config.center_type)

        self.stage_input = QComboBox()
        self.stage_input.addItems(["Infantil", "Primaria", "Infantil y Primaria", "Secundaria"])
        self._select_text(self.stage_input, self.current_config.stage)

        self.school_day_input = QComboBox()
        self.school_day_input.addItems(["Continua", "Partida"])
        self._select_text(self.school_day_input, self.current_config.school_day)

        layout.addRow("Tipo de centro", self.center_type_input)
        layout.addRow("Etapa", self.stage_input)
        layout.addRow("Tipo de jornada", self.school_day_input)
        return page

    def _page_timetable(self) -> QWidget:
        page = QWidget()
        layout = QFormLayout(page)

        self.start_time_input = QTimeEdit()
        hour, minute = [int(part) for part in self.current_config.start_time.split(":")]
        self.start_time_input.setTime(QTime(hour, minute))
        self.start_time_input.setDisplayFormat("HH:mm")

        self.sessions_input = QSpinBox()
        self.sessions_input.setRange(1, 8)
        self.sessions_input.setValue(self.current_config.sessions_per_day)

        self.duration_input = QSpinBox()
        self.duration_input.setRange(30, 90)
        self.duration_input.setValue(self.current_config.session_duration_minutes)

        self.break_after_input = QSpinBox()
        self.break_after_input.setRange(1, 8)
        self.break_after_input.setValue(self.current_config.break_after_period)

        self.break_duration_input = QSpinBox()
        self.break_duration_input.setRange(0, 60)
        self.break_duration_input.setValue(self.current_config.break_duration_minutes)

        layout.addRow("Hora de inicio", self.start_time_input)
        layout.addRow("Sesiones por día", self.sessions_input)
        layout.addRow("Duración sesión", self.duration_input)
        layout.addRow("Recreo después de P", self.break_after_input)
        layout.addRow("Duración recreo", self.break_duration_input)
        return page

    def _page_finish(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel(
            "Pulsa guardar para crear la configuración inicial del centro y generar los periodos del horario general."
        )
        label.setWordWrap(True)
        layout.addWidget(label)
        layout.addStretch()
        return page

    def current_index(self) -> int:
        return self.stack.currentIndex()

    def next_page(self) -> None:
        if self.current_index() < self.stack.count() - 1:
            self.stack.setCurrentIndex(self.current_index() + 1)
        self._refresh_buttons()

    def previous_page(self) -> None:
        if self.current_index() > 0:
            self.stack.setCurrentIndex(self.current_index() - 1)
        self._refresh_buttons()

    def finish_wizard(self) -> None:
        if self.break_after_input.value() >= self.sessions_input.value():
            QMessageBox.warning(self, "Configuración incorrecta", "El recreo debe estar antes de la última sesión.")
            return

        config = CenterConfig(
            center_name=self.center_name_input.text().strip(),
            center_code=self.center_code_input.text().strip(),
            locality=self.locality_input.text().strip(),
            province=self.province_input.text().strip(),
            school_year=self.school_year_input.text().strip(),
            center_type=self.center_type_input.currentText(),
            stage=self.stage_input.currentText(),
            school_day=self.school_day_input.currentText(),
            start_time=self.start_time_input.time().toString("HH:mm"),
            sessions_per_day=self.sessions_input.value(),
            session_duration_minutes=self.duration_input.value(),
            break_after_period=self.break_after_input.value(),
            break_duration_minutes=self.break_duration_input.value(),
        )

        self.config_service.save_config(config)

        timetable_settings = TimetableSettings(
            working_days=5,
            sessions_per_day=config.sessions_per_day,
            session_duration_minutes=config.session_duration_minutes,
            break_after_period=config.break_after_period,
            break_duration_minutes=config.break_duration_minutes,
            start_time=config.start_time,
        )
        self.timetable_service.save_settings(timetable_settings)
        self.timetable_service.save_generated_periods(timetable_settings)

        QMessageBox.information(self, "Configuración guardada", "El centro y el horario general se han configurado correctamente.")

    def _refresh_buttons(self) -> None:
        index = self.current_index()
        self.back_button.setEnabled(index > 0)
        self.next_button.setVisible(index < self.stack.count() - 1)
        self.finish_button.setVisible(index == self.stack.count() - 1)

    def _select_text(self, combo: QComboBox, text: str) -> None:
        index = combo.findText(text)
        if index >= 0:
            combo.setCurrentIndex(index)
