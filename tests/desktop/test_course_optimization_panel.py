from PySide6.QtWidgets import QApplication

from pini_desktop.ui.editor.course_optimization_panel import (
    CourseOptimizationPanel,
)


app = QApplication.instance()
if app is None:
    app = QApplication([])


class FakeResult:
    summary = "Analizadas 5 sesiones."
    best_delta = 3.5


def test_course_optimization_panel_enables_button():
    panel = CourseOptimizationPanel()

    assert not panel.button.isEnabled()

    panel.set_course(6, "6ºA")

    assert panel.button.isEnabled()
    assert "6ºA" in panel.course_label.text()


def test_course_optimization_panel_displays_result():
    panel = CourseOptimizationPanel()

    panel.set_result(FakeResult())

    assert "+3.5" in panel.summary_label.text()