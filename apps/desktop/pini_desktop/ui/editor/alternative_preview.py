from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
)


class AlternativePreviewDialog(QDialog):
    apply_requested = Signal(object)

    def __init__(self, alternative, parent=None):
        super().__init__(parent)

        self.alternative = alternative
        self.setWindowTitle("Vista previa de alternativa")

        layout = QVBoxLayout(self)

        candidate = alternative.estimated_score.candidate
        explanation = alternative.explanation

        layout.addWidget(QLabel("Vista previa del cambio"))
        layout.addWidget(QLabel(f"Sesión: {candidate.session_id}"))
        layout.addWidget(QLabel(f"Día destino: {candidate.target_day}"))
        layout.addWidget(QLabel(f"Periodo destino: {candidate.target_period}"))
        layout.addWidget(QLabel(f"Impacto: {alternative.estimated_score.delta:+.1f} puntos"))

        layout.addWidget(QLabel(explanation.summary))

        for bullet in explanation.bullets:
            layout.addWidget(QLabel(bullet))

        buttons = QHBoxLayout()

        cancel_button = QPushButton("Cancelar")
        apply_button = QPushButton("Aplicar")

        cancel_button.clicked.connect(self.reject)
        apply_button.clicked.connect(self._apply)

        buttons.addWidget(cancel_button)
        buttons.addWidget(apply_button)

        layout.addLayout(buttons)

    def _apply(self):
        self.apply_requested.emit(self.alternative)
        self.accept()