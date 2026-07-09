from __future__ import annotations

from datetime import datetime

from pini_desktop.services.editor.optimization.course_optimization_service import (
    CourseOptimizationService,
)
from pini_desktop.services.editor.optimization.history_service import HistoryEntry


class CourseOptimizationController:
    def __init__(
        self,
        panel,
        dashboard_controller,
        course_session_provider,
        optimization_service=None,
    ):
        self.panel = panel
        self.dashboard_controller = dashboard_controller
        self.course_session_provider = course_session_provider
        self.optimization_service = (
            optimization_service or CourseOptimizationService()
        )

        if hasattr(self.panel, "optimize_course_requested"):
            self.panel.optimize_course_requested.connect(
                self.optimize_course
            )

    def set_course(self, course_id: int, course_name: str = "") -> None:
        self.panel.set_course(course_id, course_name)

    def optimize_course(self, course_id: int):
        session_ids = self.course_session_provider.session_ids_for_course(
            course_id
        )

        result = self.optimization_service.optimize_course(
            course_id=course_id,
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