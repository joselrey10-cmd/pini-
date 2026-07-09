from pini_desktop.services.editor.optimization.optimization_orchestrator import (
    OptimizationOrchestrator,
    OptimizationRequest,
)


class FakeTeacherService:
    def optimize_teacher(self, teacher_id):
        return {"teacher": teacher_id}


def test_teacher_request():
    orchestrator = OptimizationOrchestrator(
        teacher_service=FakeTeacherService(),
    )

    response = orchestrator.optimize(
        OptimizationRequest(
            scope="teacher",
            target_id=5,
        )
    )

    assert response.success
    assert response.result["teacher"] == 5