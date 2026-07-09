from pini_desktop.services.editor.optimization.teacher_optimization_summary import (
    TeacherOptimizationSummaryBuilder,
)


class FakeResult:
    def __init__(self, analyzed_sessions, best_delta):
        self.analyzed_sessions = analyzed_sessions
        self.best_delta = best_delta


def test_teacher_summary_without_sessions():
    builder = TeacherOptimizationSummaryBuilder()

    text = builder.build(FakeResult(0, 0))

    assert "No se han encontrado" in text


def test_teacher_summary_with_improvement():
    builder = TeacherOptimizationSummaryBuilder()

    text = builder.build(FakeResult(3, 2.5))

    assert "+2.5" in text