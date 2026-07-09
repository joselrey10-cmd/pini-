from datetime import datetime

from PySide6.QtWidgets import QApplication

from pini_desktop.ui.editor.editor_dashboard import EditorDashboard
from pini_desktop.services.editor.optimization.history_service import HistoryEntry


app = QApplication.instance()
if app is None:
    app = QApplication([])


def test_dashboard_refresh():
    dashboard = EditorDashboard()

    history = (
        HistoryEntry(
            timestamp=datetime.now(),
            description="Mover Matemáticas",
            score_delta=2,
        ),
    )

    dashboard.refresh(history)

    assert dashboard.history_panel.list_widget.count() == 1