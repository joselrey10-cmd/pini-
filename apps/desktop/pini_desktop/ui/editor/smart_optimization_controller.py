from __future__ import annotations

from datetime import datetime

from pini_desktop.services.editor.optimization.history_service import HistoryEntry


class SmartOptimizationController:
    def __init__(self, dashboard_controller, alternative_controller):
        self.dashboard_controller = dashboard_controller
        self.alternative_controller = alternative_controller

    def optimize_session(self, session_id: int):
        self.alternative_controller.on_session_selected(session_id)

        entry = HistoryEntry(
            timestamp=datetime.now(),
            description=f"Analizadas alternativas para sesión {session_id}",
            score_delta=0.0,
        )

        self.dashboard_controller.add_entry(entry)

        return entry