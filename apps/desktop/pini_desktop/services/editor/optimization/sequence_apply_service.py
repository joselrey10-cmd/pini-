from dataclasses import dataclass

from pini_desktop.services.editor.editor_service import EditorService

@dataclass(frozen=True)
class SequenceApplyResult:
    applied: int
    failed: int
    messages: tuple[str, ...]

class SequenceApplyService:
    def __init__(self, editor_service: EditorService | None = None):
        self.editor_service = editor_service or EditorService()

    def apply(self, sequence_score) -> SequenceApplyResult:
        applied = 0
        failed = 0
        messages = []
        for step in sequence_score.sequence.steps:
            result = self.editor_service.move_session(step.session_id, step.day, step.period)
            if getattr(result, "success", False):
                applied += 1
                messages.append(f"Aplicado paso {step.order}: {step.title}")
            else:
                failed += 1
                detail = "; ".join(getattr(result, "messages", ()) or ())
                messages.append(f"No aplicado paso {step.order}: {detail or step.title}")
        return SequenceApplyResult(applied=applied, failed=failed, messages=tuple(messages))
