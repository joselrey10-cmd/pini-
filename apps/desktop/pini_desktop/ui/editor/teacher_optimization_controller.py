from __future__ import annotations

from datetime import datetime

from pini_desktop.services.editor.optimization.history_service import HistoryEntry
from pini_desktop.services.editor.optimization.teacher_optimization_service import (
    TeacherOptimizationService,
)


class TeacherOptimizationController:
    def __init__(
        self,
        panel,
        dashboard_controller,
        teacher_session_provider,
        optimization_service=None,
    ):
        self.panel = panel
        self.dashboard_controller = dashboard_controller
        self.teacher_session_provider = teacher_session_provider
        self.optimization_service = (
            optimization_service or TeacherOptimizationService()
        )

        if hasattr(self.panel, "optimize_teacher_requested"):
            self.panel.optimize_teacher_requested.connect(
                self.optimize_teacher
            )

    def set_teacher(self, teacher_id: int, teacher_name: str = "") -> None:
        self.panel.set_teacher(teacher_id, teacher_name)

    def optimize_teacher(self, teacher_id: int):
        session_ids = self.teacher_session_provider.session_ids_for_teacher(
            teacher_id
        )

        result = self.optimization_service.optimize_teacher(
            teacher_id=teacher_id,
            session_ids=session_ids,
        )

        self.panel.set_result(result)

        self.dashboard_controller.add_entry(
            HistoryEntry(
                timestamp=datetime.now(),
                description=result.summary,
                score_delta=result.best_delta,
            )
        )

        return result