from __future__ import annotations

from pini_desktop.ui.editor.alternative_panel_controller import (
    AlternativePanelController,
)


class AlternativePanelIntegration:
    def __init__(self, editor_view, editor_service):
        self.editor_view = editor_view
        self.editor_service = editor_service
        self.panel = getattr(editor_view, "alternative_panel", None)

        if self.panel is None:
            self.controller = None
            return

        self.controller = AlternativePanelController(
            panel=self.panel,
            editor_service=self.editor_service,
        )

        if hasattr(editor_view, "session_selected"):
            editor_view.session_selected.connect(
                self.controller.on_session_selected
            )

    def is_enabled(self) -> bool:
        return self.controller is not None