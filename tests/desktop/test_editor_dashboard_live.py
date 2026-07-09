from datetime import datetime

from PySide6.QtWidgets import QApplication

from pini_desktop.ui.editor.editor_dashboard import EditorDashboard
from pini_desktop.services.editor.optimization.history_service import HistoryEntry

app = QApplication.instance()
if app is None:
    app = QApplication([])


def test_dashboard_live_update():
    dashboard = EditorDashboard()

    dashboard.add_history_entry(
        HistoryEntry(
            timestamp=datetime.now(),
            description="Mover Inglés",
            score_delta=2,
        )
    )

    assert dashboard.history_panel.list_widget.count() == 1
    assert dashboard.statistics_panel.total_moves.text() == "1"