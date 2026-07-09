from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)


class AlternativeCard(QFrame):
    apply_requested = Signal(object)

    def __init__(self, alternative):
        super().__init__()

        self.alternative = alternative

        layout = QVBoxLayout(self)

        score = QLabel(
            f"⭐ {alternative.estimated_score.delta:+.1f} puntos"
        )
        summary = QLabel(alternative.explanation.summary)

        layout.addWidget(score)
        layout.addWidget(summary)

        for bullet in alternative.explanation.bullets:
            layout.addWidget(QLabel(bullet))

        button = QPushButton("Aplicar")
        button.clicked.connect(self._on_apply_clicked)

        layout.addWidget(button)

    def _on_apply_clicked(self):
        self.apply_requested.emit(self.alternative)


class AlternativePanel(QWidget):
    apply_requested = Signal(object)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

    def set_alternatives(self, alternatives):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for alternative in alternatives:
            card = AlternativeCard(alternative)
            card.apply_requested.connect(self.apply_requested.emit)
            self.layout.addWidget(card)

        self.layout.addStretch()