from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QFormLayout, QLabel, QListWidget, QMessageBox, QPushButton, QSpinBox, QVBoxLayout, QWidget

from pini_desktop.services.editor.optimization.sequence_apply_service import SequenceApplyService
from pini_desktop.services.editor.optimization.sequence_optimizer import SequenceOptimizer
from pini_desktop.services.editor.optimization.zone_definition import ZoneDefinition
from pini_desktop.ui.views.sequence_preview_dialog import SequencePreviewDialog
from pini_desktop.ui.views.sequence_report_dialog import SequenceReportDialog


class SequenceOptimizerPanel(QWidget):
    sequenceApplied = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.optimizer = SequenceOptimizer()
        self.apply_service = SequenceApplyService()
        self.current_sequences = []

        title = QLabel("Cadenas inteligentes")
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
        self.depth = QSpinBox()
        self.depth.setRange(1, 6)
        self.depth.setValue(3)

        form = QFormLayout()
        form.addRow("Tipo", self.zone_type)
        form.addRow("ID entidad", self.entity_id)
        form.addRow("Día", self.day)
        form.addRow("Desde periodo", self.start_period)
        form.addRow("Hasta periodo", self.end_period)
        form.addRow("Profundidad", self.depth)

        search_button = QPushButton("Buscar cadenas")
        search_button.clicked.connect(self.search_sequences)
        preview_button = QPushButton("Previsualizar cadena")
        preview_button.clicked.connect(self.preview_selected)
        report_button = QPushButton("Ver informe IA")
        report_button.clicked.connect(self.report_selected)
        apply_button = QPushButton("Aplicar cadena seleccionada")
        apply_button.clicked.connect(self.apply_selected)

        self.summary = QLabel("Sin cadenas calculadas.")
        self.summary.setWordWrap(True)
        self.list_widget = QListWidget()

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(search_button)
        layout.addWidget(preview_button)
        layout.addWidget(report_button)
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

    def search_sequences(self):
        zone = self.build_zone()
        result = self.optimizer.optimize(zone, max_depth=self.depth.value(), limit=5)
        self.current_sequences = list(result.sequences)
        self.list_widget.clear()
        if not result.has_sequences:
            self.summary.setText("No se han encontrado cadenas de mejora.")
            return

        best = result.best
        self.summary.setText(
            f"Cadenas encontradas: {len(self.current_sequences)} · "
            f"Mejor score: {best.score if best else 0} · "
            f"Mejora: +{best.sequence.estimated_delta if best else 0}"
        )
        for index, item in enumerate(self.current_sequences, start=1):
            self.list_widget.addItem(
                f"#{index} · {item.recommendation} · score {item.score} · "
                f"riesgo {item.risk} · pasos {item.sequence.length} · "
                f"delta +{item.sequence.estimated_delta}"
            )

    def selected_sequence(self):
        row = self.list_widget.currentRow()
        if row < 0 or row >= len(self.current_sequences):
            QMessageBox.information(self, "Cadena", "Selecciona una cadena.")
            return None
        return self.current_sequences[row]

    def preview_selected(self):
        item = self.selected_sequence()
        if item is not None:
            SequencePreviewDialog(item, self).exec()

    def report_selected(self):
        item = self.selected_sequence()
        if item is not None:
            SequenceReportDialog(item, self).exec()

    def apply_selected(self):
        item = self.selected_sequence()
        if item is None:
            return
        dialog = SequencePreviewDialog(item, self)
        if dialog.exec() != dialog.Accepted:
            self.summary.setText("Aplicación cancelada.")
            return
        result = self.apply_service.apply(item)
        self.summary.setText(f"Cadena aplicada. Correctas: {result.applied}. Fallidas: {result.failed}.")
        self.sequenceApplied.emit(result)
