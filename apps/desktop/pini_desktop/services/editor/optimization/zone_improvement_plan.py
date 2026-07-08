from dataclasses import dataclass

from pini_desktop.services.editor.editor_service import EditorService
from pini_desktop.services.editor.optimization.iterative_zone_search import IterativeZoneSearchResult


@dataclass(frozen=True)
class ZoneImprovementAction:
    order: int
    session_id: int
    day: int
    period: int
    estimated_delta: float
    title: str


@dataclass(frozen=True)
class ZoneImprovementPlan:
    zone_label: str
    actions: tuple[ZoneImprovementAction, ...]
    estimated_delta: float

    @property
    def has_actions(self) -> bool:
        return bool(self.actions)


@dataclass(frozen=True)
class ZoneImprovementApplyResult:
    applied: int
    failed: int
    messages: tuple[str, ...]


class ZoneImprovementPlanner:
    def build_plan(self, search_result: IterativeZoneSearchResult) -> ZoneImprovementPlan:
        actions = tuple(
            ZoneImprovementAction(
                order=step.iteration,
                session_id=step.suggestion.session_id,
                day=step.suggestion.day,
                period=step.suggestion.period,
                estimated_delta=step.suggestion.estimated_delta,
                title=step.suggestion.title,
            )
            for step in search_result.steps
        )
        return ZoneImprovementPlan(
            zone_label=search_result.zone.describe(),
            actions=actions,
            estimated_delta=search_result.accumulated_delta,
        )


class ZoneImprovementApplyService:
    def __init__(self, editor_service: EditorService | None = None):
        self.editor_service = editor_service or EditorService()

    def apply_plan(self, plan: ZoneImprovementPlan) -> ZoneImprovementApplyResult:
        applied = 0
        failed = 0
        messages = []

        for action in plan.actions:
            result = self.editor_service.move_session(action.session_id, action.day, action.period)
            if getattr(result, "success", False):
                applied += 1
                messages.append(f"Aplicada acción {action.order}: {action.title}")
            else:
                failed += 1
                joined = "; ".join(getattr(result, "messages", ()) or ())
                messages.append(f"No aplicada acción {action.order}: {joined or action.title}")

        return ZoneImprovementApplyResult(
            applied=applied,
            failed=failed,
            messages=tuple(messages),
        )
