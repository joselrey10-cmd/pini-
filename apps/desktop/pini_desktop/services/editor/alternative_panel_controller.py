from __future__ import annotations

from pini_desktop.services.editor.optimization.alternative_generator import (
    AlternativeGenerator,
)


class AlternativePanelController:
    def __init__(self, panel, editor_service):
        self.panel = panel
        self.editor_service = editor_service
        self.generator = AlternativeGenerator()

    def on_session_selected(self, session_id: int) -> None:
        alternatives = self.generator.generate_for_session(
            session_id=session_id,
            current_day=1,
            current_period=1,
            limit=5,
        )

        self.panel.set_alternatives(alternatives)