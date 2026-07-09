from pini_desktop.ui.editor.course_optimization_controller import (
    CourseOptimizationController,
)


class FakeSignal:
    def __init__(self):
        self.callback = None

    def connect(self, callback):
        self.callback = callback


class FakePanel:
    def __init__(self):
        self.optimize_course_requested = FakeSignal()
        self.course = None
        self.result = None

    def set_course(self, course_id, course_name=""):
        self.course = (course_id, course_name)

    def set_result(self, result):
        self.result = result


class FakeDashboardController:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)


class FakeProvider:
    def session_ids_for_course(self, course_id):
        return [1, 2, 3]


class FakeResult:
    course_id = 6
    analyzed_sessions = 3
    best_delta = 3.5
    summary = "Analizadas 3 sesiones del curso 6."


class FakeOptimizationService:
    def optimize_course(self, course_id, session_ids):
        self.called = (course_id, session_ids)
        return FakeResult()


def test_course_optimization_controller_sets_course():
    panel = FakePanel()
    controller = CourseOptimizationController(
        panel=panel,
        dashboard_controller=FakeDashboardController(),
        course_session_provider=FakeProvider(),
        optimization_service=FakeOptimizationService(),
    )

    controller.set_course(6, "6ºA")

    assert panel.course == (6, "6ºA")


def test_course_optimization_controller_optimizes_course():
    panel = FakePanel()
    dashboard = FakeDashboardController()
    service = FakeOptimizationService()

    controller = CourseOptimizationController(
        panel=panel,
        dashboard_controller=dashboard,
        course_session_provider=FakeProvider(),
        optimization_service=service,
    )

    result = controller.optimize_course(6)

    assert result.course_id == 6
    assert panel.result == result
    assert dashboard.entries
    assert service.called == (6, [1, 2, 3])