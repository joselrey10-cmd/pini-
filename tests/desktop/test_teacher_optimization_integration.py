from pini_desktop.ui.editor.teacher_optimization_integration import (
    TeacherOptimizationIntegration,
)


class FakeSignal:
    def __init__(self):
        self.callback = None

    def connect(self, callback):
        self.callback = callback


class FakePanel:
    optimize_teacher_requested = FakeSignal()

    def set_teacher(self, teacher_id, teacher_name=""):
        self.teacher = (teacher_id, teacher_name)

    def set_result(self, result):
        self.result = result


class FakeEditorView:
    def __init__(self):
        self.teacher_optimization_panel = FakePanel()
        self.teacher_selected = FakeSignal()


class FakeDashboardController:
    def add_entry(self, entry):
        pass


class FakeProvider:
    def session_ids_for_teacher(self, teacher_id):
        return []


def test_teacher_optimization_integration_enabled():
    view = FakeEditorView()

    integration = TeacherOptimizationIntegration(
        editor_view=view,
        dashboard_controller=FakeDashboardController(),
        teacher_session_provider=FakeProvider(),
    )

    assert integration.is_enabled()
    assert view.teacher_selected.callback is not None