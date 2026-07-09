from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel


class SmartOptimizationPanel(QWidget):
    optimize_requested = Signal(int)

    def __init__(self):
        super().__init__()

        self.selected_session_id = None

        layout = QVBoxLayout(self)

        self.label = QLabel("Selecciona una sesión para optimizar")
        self.button = QPushButton("Optimizar sesión")
        self.button.setEnabled(False)

        self.button.clicked.connect(self._emit_optimize)

        layout.addWidget(self.label)
        layout.addWidget(self.button)

    def set_selected_session(self, session_id: int):
        self.selected_session_id = session_id
        self.label.setText(f"Sesión seleccionada: {session_id}")
        self.button.setEnabled(True)

    def _emit_optimize(self):
        if self.selected_session_id is not None:
            self.optimize_requested.emit(self.selected_session_id)