from pini_desktop.ui.editor.teacher_optimization_controller import (
    TeacherOptimizationController,
)


class FakeSignal:
    def __init__(self):
        self.callback = None

    def connect(self, callback):
        self.callback = callback


class FakePanel:
    def __init__(self):
        self.optimize_teacher_requested = FakeSignal()
        self.teacher = None
        self.result = None

    def set_teacher(self, teacher_id, teacher_name=""):
        self.teacher = (teacher_id, teacher_name)

    def set_result(self, result):
        self.result = result


class FakeDashboardController:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)


class FakeProvider:
    def session_ids_for_teacher(self, teacher_id):
        return [1, 2, 3]


class FakeResult:
    teacher_id = 4
    analyzed_sessions = 3
    best_delta = 2.5
    summary = "Analizadas 3 sesiones del profesor 4."


class FakeOptimizationService:
    def optimize_teacher(self, teacher_id, session_ids):
        self.called = (teacher_id, session_ids)
        return FakeResult()


def test_teacher_optimization_controller_sets_teacher():
    panel = FakePanel()
    controller = TeacherOptimizationController(
        panel=panel,
        dashboard_controller=FakeDashboardController(),
        teacher_session_provider=FakeProvider(),
        optimization_service=FakeOptimizationService(),
    )

    controller.set_teacher(4, "María")

    assert panel.teacher == (4, "María")


def test_teacher_optimization_controller_optimizes_teacher():
    panel = FakePanel()
    dashboard = FakeDashboardController()
    service = FakeOptimizationService()

    controller = TeacherOptimizationController(
        panel=panel,
        dashboard_controller=dashboard,
        teacher_session_provider=FakeProvider(),
        optimization_service=service,
    )

    result = controller.optimize_teacher(4)

    assert result.teacher_id == 4
    assert panel.result == result
    assert dashboard.entries
    assert service.called == (4, [1, 2, 3])