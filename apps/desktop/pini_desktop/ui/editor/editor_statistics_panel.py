from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLabel,
)


class EditorStatisticsPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QFormLayout(self)

        self.total_moves = QLabel("0")
        self.score_gain = QLabel("0")
        self.best_score = QLabel("0")

        layout.addRow("Movimientos:", self.total_moves)
        layout.addRow("Mejora total:", self.score_gain)
        layout.addRow("Mejor puntuación:", self.best_score)

    def update_statistics(self, history):
        total = len(history)

        gain = sum(getattr(item, "score_delta", 0) for item in history)

        if history:
            best = max(getattr(item, "score", 0) for item in history)
        else:
            best = 0

        self.total_moves.setText(str(total))
        self.score_gain.setText(f"{gain:+.1f}")
        self.best_score.setText(f"{best:.1f}")