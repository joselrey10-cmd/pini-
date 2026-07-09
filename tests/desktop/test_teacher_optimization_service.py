from pini_desktop.services.editor.optimization.teacher_optimization_service import (
    TeacherOptimizationService,
)


class FakeEstimatedScore:
    def __init__(self, delta):
        self.delta = delta


class FakeAlternative:
    def __init__(self, delta):
        self.estimated_score = FakeEstimatedScore(delta)


class FakeGenerator:
    def generate_for_session(self, session_id, current_day, current_period, limit):
        return [
            FakeAlternative(1.0),
            FakeAlternative(2.5),
        ]


def test_teacher_optimization_service_analyzes_teacher_sessions():
    service = TeacherOptimizationService(alternative_generator=FakeGenerator())

    result = service.optimize_teacher(teacher_id=3, session_ids=[1, 2, 3])

    assert result.teacher_id == 3
    assert result.analyzed_sessions == 3
    assert result.best_delta == 2.5