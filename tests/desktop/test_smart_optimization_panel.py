from PySide6.QtWidgets import QApplication

from pini_desktop.ui.editor.smart_optimization_panel import SmartOptimizationPanel


app = QApplication.instance()
if app is None:
    app = QApplication([])


def test_smart_optimization_panel_enables_button():
    panel = SmartOptimizationPanel()

    assert not panel.button.isEnabled()

    panel.set_selected_session(12)

    assert panel.button.isEnabled()
    assert "12" in panel.label.text()