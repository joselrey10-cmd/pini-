from __future__ import annotations

from pini_desktop.ui.editor.course_optimization_controller import (
    CourseOptimizationController,
)


class CourseOptimizationIntegration:
    def __init__(
        self,
        editor_view,
        dashboard_controller,
        course_session_provider,
        optimization_service=None,
    ):
        self.editor_view = editor_view
        self.panel = getattr(editor_view, "course_optimization_panel", None)

        if self.panel is None:
            self.controller = None
            return

        self.controller = CourseOptimizationController(
            panel=self.panel,
            dashboard_controller=dashboard_controller,
            course_session_provider=course_session_provider,
            optimization_service=optimization_service,
        )

        if hasattr(editor_view, "course_selected"):
            editor_view.course_selected.connect(self.controller.set_course)

    def is_enabled(self) -> bool:
        return self.controller is not None