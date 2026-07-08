from __future__ import annotations

from dataclasses import dataclass

from .simulation_snapshot import SimulationSnapshot


@dataclass(frozen=True)
class SimulationComparison:
    before: SimulationSnapshot
    after: SimulationSnapshot
    score_delta: float
    conflict_delta: int
    teacher_gap_delta: int
    course_gap_delta: int
    moved_sessions: int
    summary: str

    @property
    def improves_score(self) -> bool:
        return self.score_delta > 0

    @property
    def adds_conflicts(self) -> bool:
        return self.conflict_delta > 0


class SimulationComparisonService:
    def compare(self, before: SimulationSnapshot, after: SimulationSnapshot) -> SimulationComparison:
        before_by_id = {item.id: item for item in before.sessions}
        after_by_id = {item.id: item for item in after.sessions}
        moved = 0
        for session_id in set(before_by_id).intersection(after_by_id):
            a = before_by_id[session_id]
            b = after_by_id[session_id]
            if a.day != b.day or a.period != b.period:
                moved += 1

        score_delta = round(after.metrics.score - before.metrics.score, 2)
        conflict_delta = after.metrics.total_conflicts - before.metrics.total_conflicts
        teacher_gap_delta = after.metrics.teacher_gaps - before.metrics.teacher_gaps
        course_gap_delta = after.metrics.course_gaps - before.metrics.course_gaps
        summary = (
            f"Score {before.metrics.score} → {after.metrics.score} "
            f"({score_delta:+}); conflictos {conflict_delta:+}; sesiones movidas {moved}."
        )
        return SimulationComparison(
            before=before,
            after=after,
            score_delta=score_delta,
            conflict_delta=conflict_delta,
            teacher_gap_delta=teacher_gap_delta,
            course_gap_delta=course_gap_delta,
            moved_sessions=moved,
            summary=summary,
        )
