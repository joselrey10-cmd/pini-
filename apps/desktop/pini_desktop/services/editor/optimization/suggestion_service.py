from dataclasses import dataclass

from pini_desktop.services.editor.editor_service import EditorService
from pini_desktop.services.editor.optimization.local_optimizer import LocalOptimizationSuggestion


@dataclass(frozen=True)
class SuggestionApplyResult:
    success: bool
    message: str
    editor_result: object | None = None


class EditorSuggestionService:
    """Aplica sugerencias generadas por el optimizador local.

    En esta primera versión solo ejecuta sugerencias que ya traen una acción
    concreta en el payload. Las sugerencias de tipo review/keep/inspect quedan
    como recomendaciones informativas.
    """

    def __init__(self, editor_service: EditorService | None = None):
        self.editor_service = editor_service or EditorService()

    def apply(self, suggestion: LocalOptimizationSuggestion) -> SuggestionApplyResult:
        if suggestion.action_type == "move":
            payload = suggestion.payload
            result = self.editor_service.move_session(
                int(payload["session_id"]),
                int(payload["day"]),
                int(payload["period"]),
            )
            return SuggestionApplyResult(result.success, "Movimiento sugerido aplicado.", result)

        if suggestion.action_type == "swap":
            payload = suggestion.payload
            result = self.editor_service.swap_sessions(
                int(payload["first_session_id"]),
                int(payload["second_session_id"]),
            )
            return SuggestionApplyResult(result.success, "Intercambio sugerido aplicado.", result)

        return SuggestionApplyResult(
            False,
            "Esta sugerencia es informativa y todavía no tiene una acción automática asociada.",
            None,
        )
