from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
)


class EditorHistoryPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Historial de optimización")

        layout = QVBoxLayout(self)

        title = QLabel("Historial de optimización")
        self.list_widget = QListWidget()

        layout.addWidget(title)
        layout.addWidget(self.list_widget)

    def set_entries(self, entries):
        self.list_widget.clear()

        for entry in entries:
            time_text = entry.timestamp.strftime("%H:%M")
            delta_text = f"{entry.score_delta:+.1f}"

            item = QListWidgetItem(
                f"{time_text} · {delta_text} puntos · {entry.description}"
            )

            self.list_widget.addItem(item)