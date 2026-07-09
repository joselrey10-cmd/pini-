from pini_desktop.ui.editor.course_optimization_integration import (
    CourseOptimizationIntegration,
)


class FakeSignal:
    def __init__(self):
        self.callback = None

    def connect(self, callback):
        self.callback = callback


class FakePanel:
    def __init__(self):
        self.optimize_course_requested = FakeSignal()

    def set_course(self, course_id, course_name=""):
        self.course = (course_id, course_name)

    def set_result(self, result):
        self.result = result


class FakeEditorView:
    def __init__(self):
        self.course_optimization_panel = FakePanel()
        self.course_selected = FakeSignal()


class FakeDashboardController:
    def add_entry(self, entry):
        pass


class FakeProvider:
    def session_ids_for_course(self, course_id):
        return []


def test_course_optimization_integration_enabled():
    view = FakeEditorView()

    integration = CourseOptimizationIntegration(
        editor_view=view,
        dashboard_controller=FakeDashboardController(),
        course_session_provider=FakeProvider(),
    )

    assert integration.is_enabled()
    assert view.course_selected.callback is not None