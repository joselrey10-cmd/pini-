from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QFormLayout, QLabel, QListWidget, QMessageBox, QPushButton, QSpinBox, QVBoxLayout, QWidget

from pini_desktop.services.editor.optimization.iterative_zone_search import IterativeZoneSearch
from pini_desktop.services.editor.optimization.zone_definition import ZoneDefinition
from pini_desktop.services.editor.optimization.zone_improvement_plan import ZoneImprovementApplyService, ZoneImprovementPlanner
from pini_desktop.ui.views.zone_plan_preview_dialog import ZonePlanPreviewDialog


class ZoneIterativePanel(QWidget):
    planApplied = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.search_engine = IterativeZoneSearch()
        self.planner = ZoneImprovementPlanner()
        self.apply_service = ZoneImprovementApplyService()
        self.current_plan = None

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

        search_button = QPushButton("Buscar mejoras")
        search_button.clicked.connect(self.run_search)

        preview_button = QPushButton("Previsualizar plan")
        preview_button.clicked.connect(self.preview_plan)

        apply_button = QPushButton("Aplicar plan")
        apply_button.clicked.connect(self.apply_plan)

        self.summary = QLabel("Sin búsqueda.")
        self.summary.setWordWrap(True)

        self.list_widget = QListWidget()

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(search_button)
        layout.addWidget(preview_button)
        layout.addWidget(apply_button)
        layout.addWidget(self.summary)
        layout.addWidget(self.list_widget)

    def build_zone(self):
        ztype = self.zone_type.currentData()
        return ZoneDefinition(
            zone_type=ztype,
            entity_id=self.entity_id.value() if ztype != "time" else None,
            day=self.day.value() if ztype == "time" else None,
            start_period=self.start_period.value() if ztype == "time" else None,
            end_period=self.end_period.value() if ztype == "time" else None,
            label=str(self.entity_id.value()),
        )

    def run_search(self):
        zone = self.build_zone()
        result = self.search_engine.search(zone, max_iterations=self.iterations.value())
        self.current_plan = self.planner.build_plan(result)

        self.summary.setText(
            f"{zone.describe()} · Iteraciones: {result.iterations} · "
            f"Mejora acumulada estimada: +{result.accumulated_delta}"
        )

        self.list_widget.clear()
        for action in self.current_plan.actions:
            self.list_widget.addItem(
                f"#{action.order} · {action.title} · sesión {action.session_id} · "
                f"+{action.estimated_delta}"
            )

    def preview_plan(self):
        if self.current_plan is None or not self.current_plan.has_actions:
            QMessageBox.information(self, "Plan de mejora", "Primero busca mejoras.")
            return
        ZonePlanPreviewDialog(self.current_plan, self).exec()

    def apply_plan(self):
        if self.current_plan is None or not self.current_plan.has_actions:
            QMessageBox.information(self, "Plan de mejora", "No hay plan para aplicar.")
            return

        dialog = ZonePlanPreviewDialog(self.current_plan, self)
        if dialog.exec() != dialog.Accepted:
            self.summary.setText("Aplicación cancelada.")
            return

        result = self.apply_service.apply_plan(self.current_plan)
        self.summary.setText(
            f"Plan aplicado. Acciones correctas: {result.applied}. Fallidas: {result.failed}."
        )
        self.planApplied.emit(result)
