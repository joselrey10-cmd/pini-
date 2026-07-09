from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ApplyResult:
    applied: bool
    reason: str = ""


class AlternativeApplyService:
    def apply(self, alternative) -> ApplyResult:
        estimated = getattr(alternative, "estimated_score", None)

        if estimated is None:
            return ApplyResult(False, "La alternativa no tiene puntuación.")

        candidate = estimated.candidate
        schedule = candidate.schedule

        schedule.move_session(
            candidate.session_id,
            candidate.target_day,
            candidate.target_period,
        )

        return ApplyResult(True)