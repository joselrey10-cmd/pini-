from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
)

from pini_desktop.ui.editor.editor_history_panel import EditorHistoryPanel
from pini_desktop.ui.editor.editor_statistics_panel import EditorStatisticsPanel


class EditorDashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.history_panel = EditorHistoryPanel()
        self.statistics_panel = EditorStatisticsPanel()

        self._history = []

        left = QVBoxLayout()
        left.addWidget(self.statistics_panel)

        right = QVBoxLayout()
        right.addWidget(self.history_panel)

        layout = QHBoxLayout(self)
        layout.addLayout(left, 1)
        layout.addLayout(right, 2)

    def refresh(self, history):
        self._history = list(history)
        self.history_panel.set_entries(history)
        self.statistics_panel.update_statistics(history)

    def add_history_entry(self, entry):
        self._history.append(entry)
        self.refresh(self._history)