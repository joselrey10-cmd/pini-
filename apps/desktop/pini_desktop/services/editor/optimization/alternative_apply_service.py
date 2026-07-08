from dataclasses import dataclass

from pini_desktop.services.editor.editor_service import EditorService
from pini_desktop.services.editor.optimization.alternative_generator import EditorAlternative


@dataclass(frozen=True)
class AlternativeApplyResult:
    success: bool
    message: str
    editor_result: object | None = None


class AlternativeApplyService:
    def __init__(self, editor_service: EditorService | None = None):
        self.editor_service = editor_service or EditorService()

    def apply(self, alternative: EditorAlternative) -> AlternativeApplyResult:
        candidate = alternative.candidate
        result = self.editor_service.move_session(
            int(candidate.session_id),
            int(candidate.day),
            int(candidate.period),
        )
        return AlternativeApplyResult(
            success=result.success,
            message="Alternativa aplicada." if result.success else "No se ha podido aplicar la alternativa.",
            editor_result=result,
        )
