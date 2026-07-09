from pini_desktop.ui.editor.smart_optimization_controller import (
    SmartOptimizationController,
)


class FakeDashboardController:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)


class FakeAlternativeController:
    def __init__(self):
        self.selected = None

    def on_session_selected(self, session_id):
        self.selected = session_id


def test_smart_optimization_controller_analyzes_session():
    dashboard = FakeDashboardController()
    alternatives = FakeAlternativeController()

    controller = SmartOptimizationController(dashboard, alternatives)

    entry = controller.optimize_session(7)

    assert alternatives.selected == 7
    assert dashboard.entries[0] == entry
    assert "sesión 7" in entry.description