from datetime import datetime

from PySide6.QtWidgets import QApplication

from pini_desktop.ui.editor.editor_statistics_panel import EditorStatisticsPanel
from pini_desktop.services.editor.optimization.history_service import HistoryEntry


app = QApplication.instance()
if app is None:
    app = QApplication([])


def test_statistics_panel_updates():
    panel = EditorStatisticsPanel()

    history = [
        HistoryEntry(
            timestamp=datetime.now(),
            description="Cambio 1",
            score_delta=2,
        ),
        HistoryEntry(
            timestamp=datetime.now(),
            description="Cambio 2",
            score_delta=1,
        ),
    ]

    panel.update_statistics(history)

    assert panel.total_moves.text() == "2"
    assert panel.score_gain.text() == "+3.0"