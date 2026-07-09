from datetime import datetime

from PySide6.QtWidgets import QApplication

from pini_desktop.ui.editor.editor_history_panel import EditorHistoryPanel
from pini_desktop.services.editor.optimization.history_service import HistoryEntry


app = QApplication.instance()
if app is None:
    app = QApplication([])


def test_editor_history_panel_displays_entries():
    panel = EditorHistoryPanel()

    entries = (
        HistoryEntry(
            timestamp=datetime(2026, 1, 1, 13, 22),
            description="Mover Matemáticas",
            score_delta=2.5,
        ),
    )

    panel.set_entries(entries)

    assert panel.list_widget.count() == 1
    assert "Mover Matemáticas" in panel.list_widget.item(0).text()