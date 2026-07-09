from pini_desktop.services.editor.optimization.course_optimization_summary import (
    CourseOptimizationSummaryBuilder,
)


class FakeResult:
    def __init__(self, analyzed_sessions, best_delta):
        self.analyzed_sessions = analyzed_sessions
        self.best_delta = best_delta


def test_course_summary_without_sessions():
    builder = CourseOptimizationSummaryBuilder()

    text = builder.build(FakeResult(0, 0))

    assert "No se han encontrado" in text


def test_course_summary_with_improvement():
    builder = CourseOptimizationSummaryBuilder()

    text = builder.build(FakeResult(5, 3.5))

    assert "+3.5" in text