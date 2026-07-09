from PySide6.QtWidgets import QApplication

from pini_desktop.ui.editor.teacher_optimization_panel import (
    TeacherOptimizationPanel,
)


app = QApplication.instance()
if app is None:
    app = QApplication([])


class FakeResult:
    summary = "Analizadas 3 sesiones."
    best_delta = 2.5


def test_teacher_optimization_panel_enables_button():
    panel = TeacherOptimizationPanel()

    assert not panel.button.isEnabled()

    panel.set_teacher(4, "María")

    assert panel.button.isEnabled()
    assert "María" in panel.teacher_label.text()


def test_teacher_optimization_panel_displays_result():
    panel = TeacherOptimizationPanel()

    panel.set_result(FakeResult())

    assert "+2.5" in panel.summary_label.text()