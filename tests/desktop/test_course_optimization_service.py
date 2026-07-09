from pini_desktop.services.editor.optimization.course_optimization_service import (
    CourseOptimizationService,
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
            FakeAlternative(3.5),
        ]


def test_course_optimization_service_analyzes_course_sessions():
    service = CourseOptimizationService(alternative_generator=FakeGenerator())

    result = service.optimize_course(course_id=6, session_ids=[1, 2, 3])

    assert result.course_id == 6
    assert result.analyzed_sessions == 3
    assert result.best_delta == 3.5