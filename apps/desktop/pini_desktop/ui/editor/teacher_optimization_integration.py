from __future__ import annotations

from pini_desktop.ui.editor.teacher_optimization_controller import (
    TeacherOptimizationController,
)


class TeacherOptimizationIntegration:
    def __init__(
        self,
        editor_view,
        dashboard_controller,
        teacher_session_provider,
        optimization_service=None,
    ):
        self.editor_view = editor_view

        self.panel = getattr(editor_view, "teacher_optimization_panel", None)

        if self.panel is None:
            self.controller = None
            return

        self.controller = TeacherOptimizationController(
            panel=self.panel,
            dashboard_controller=dashboard_controller,
            teacher_session_provider=teacher_session_provider,
            optimization_service=optimization_service,
        )

        if hasattr(editor_view, "teacher_selected"):
            editor_view.teacher_selected.connect(self.controller.set_teacher)

    def is_enabled(self) -> bool:
        return self.controller is not None