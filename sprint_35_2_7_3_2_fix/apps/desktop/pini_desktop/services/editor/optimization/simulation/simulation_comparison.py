from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationComparison:
    before_score: float
    after_score: float
    delta_score: float
    teacher_gaps_delta: int
    course_gaps_delta: int
    room_conflicts_delta: int
    last_periods_delta: int
    summary: str
    moved_sessions: int = 0

    @property
    def improves(self) -> bool:
        return self.delta_score > 0 and self.room_conflicts_delta <= 0


class SimulationComparisonService:
    def compare(self, before_snapshot, after_snapshot) -> SimulationComparison:
        before = before_snapshot.metrics
        after = after_snapshot.metrics

        delta_score = round(after.score - before.score, 2)
        teacher_gaps_delta = after.teacher_gaps - before.teacher_gaps
        course_gaps_delta = after.course_gaps - before.course_gaps
        room_conflicts_delta = after.room_conflicts - before.room_conflicts
        last_periods_delta = after.last_periods - before.last_periods

        if delta_score > 0:
            summary = f"La simulación mejora el score global en +{delta_score}."
        elif delta_score < 0:
            summary = f"La simulación empeora el score global en {delta_score}."
        else:
            summary = "La simulación mantiene el mismo score global."

        before_positions = getattr(before_snapshot, "positions", {}) or {}
        after_positions = getattr(after_snapshot, "positions", {}) or {}
        moved_sessions = sum(
            1
            for session_id, position in after_positions.items()
            if before_positions.get(session_id) != position
        )

        return SimulationComparison(
            before_score=before.score,
            after_score=after.score,
            delta_score=delta_score,
            teacher_gaps_delta=teacher_gaps_delta,
            course_gaps_delta=course_gaps_delta,
            room_conflicts_delta=room_conflicts_delta,
            last_periods_delta=last_periods_delta,
            summary=summary,
            moved_sessions=moved_sessions,
        )
