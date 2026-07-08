from PySide6.QtWidgets import QComboBox, QFormLayout, QLabel, QListWidget, QPushButton, QSpinBox, QVBoxLayout, QWidget

from pini_desktop.services.editor.optimization.iterative_zone_search import IterativeZoneSearch
from pini_desktop.services.editor.optimization.zone_definition import ZoneDefinition


class ZoneIterativePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.search_engine = IterativeZoneSearch()

        title = QLabel("Búsqueda iterativa por zonas")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.zone_type = QComboBox()
        self.zone_type.addItem("Profesor", "teacher")
        self.zone_type.addItem("Curso", "course")
        self.zone_type.addItem("Aula", "room")
        self.zone_type.addItem("Tramo horario", "time")

        self.entity_id = QSpinBox()
        self.entity_id.setRange(1, 999999)

        self.day = QSpinBox()
        self.day.setRange(1, 5)

        self.start_period = QSpinBox()
        self.start_period.setRange(1, 8)
        self.start_period.setValue(1)

        self.end_period = QSpinBox()
        self.end_period.setRange(1, 8)
        self.end_period.setValue(6)

        self.iterations = QSpinBox()
        self.iterations.setRange(1, 20)
        self.iterations.setValue(3)

        form = QFormLayout()
        form.addRow("Tipo", self.zone_type)
        form.addRow("ID entidad", self.entity_id)
        form.addRow("Día", self.day)
        form.addRow("Desde periodo", self.start_period)
        form.addRow("Hasta periodo", self.end_period)
        form.addRow("Iteraciones", self.iterations)

        button = QPushButton("Buscar mejoras")
        button.clicked.connect(self.run_search)

        self.summary = QLabel("Sin búsqueda.")
        self.summary.setWordWrap(True)

        self.list_widget = QListWidget()

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(button)
        layout.addWidget(self.summary)
        layout.addWidget(self.list_widget)

    def run_search(self):
        ztype = self.zone_type.currentData()
        zone = ZoneDefinition(
            zone_type=ztype,
            entity_id=self.entity_id.value() if ztype != "time" else None,
            day=self.day.value() if ztype == "time" else None,
            start_period=self.start_period.value() if ztype == "time" else None,
            end_period=self.end_period.value() if ztype == "time" else None,
            label=str(self.entity_id.value()),
        )

        result = self.search_engine.search(zone, max_iterations=self.iterations.value())

        self.summary.setText(
            f"{zone.describe()} · Iteraciones: {result.iterations} · "
            f"Mejora acumulada estimada: +{result.accumulated_delta}"
        )

        self.list_widget.clear()
        for step in result.steps:
            self.list_widget.addItem(
                f"#{step.iteration} · {step.suggestion.title} · sesión {step.suggestion.session_id} · "
                f"+{step.suggestion.estimated_delta} · acumulado +{step.accumulated_delta}"
            )
