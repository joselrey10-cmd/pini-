from PySide6.QtWidgets import QComboBox, QFormLayout, QLabel, QListWidget, QPushButton, QSpinBox, QVBoxLayout, QWidget

from pini_desktop.services.editor.optimization.zone_definition import ZoneDefinition
from pini_desktop.services.editor.optimization.zone_optimizer import ZoneOptimizer

class ZoneOptimizationPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.optimizer = ZoneOptimizer()

        title = QLabel("Optimización por zonas")
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

        form = QFormLayout()
        form.addRow("Tipo", self.zone_type)
        form.addRow("ID entidad", self.entity_id)
        form.addRow("Día", self.day)
        form.addRow("Desde periodo", self.start_period)
        form.addRow("Hasta periodo", self.end_period)

        button = QPushButton("Optimizar zona")
        button.clicked.connect(self.optimize_zone)

        self.summary = QLabel("Sin optimización.")
        self.summary.setWordWrap(True)
        self.list_widget = QListWidget()

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(button)
        layout.addWidget(self.summary)
        layout.addWidget(self.list_widget)

    def optimize_zone(self):
        ztype = self.zone_type.currentData()
        zone = ZoneDefinition(
            zone_type=ztype,
            entity_id=self.entity_id.value() if ztype != "time" else None,
            day=self.day.value() if ztype == "time" else None,
            start_period=self.start_period.value() if ztype == "time" else None,
            end_period=self.end_period.value() if ztype == "time" else None,
            label=str(self.entity_id.value()),
        )
        result = self.optimizer.optimize(zone)
        self.summary.setText(
            f"{zone.describe()} · Score: {result.before.score} · Huecos: {result.before.gaps} · "
            f"Últimas horas: {result.before.last_periods} · Mejor delta: +{result.best_delta}"
        )
        self.list_widget.clear()
        for s in result.suggestions:
            self.list_widget.addItem(f"{s.title} · sesión {s.session_id} · +{s.estimated_delta}")
