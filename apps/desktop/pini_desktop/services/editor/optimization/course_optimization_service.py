from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CourseOptimizationResult:
    course_id: int
    analyzed_sessions: int
    best_delta: float
    summary: str


class CourseOptimizationService:
    def __init__(self, alternative_generator=None):
        self.alternative_generator = alternative_generator

    def optimize_course(self, course_id: int, session_ids) -> CourseOptimizationResult:
        session_ids = tuple(session_ids)
        analyzed = len(session_ids)

        if analyzed == 0:
            return CourseOptimizationResult(
                course_id=course_id,
                analyzed_sessions=0,
                best_delta=0.0,
                summary="No hay sesiones para optimizar.",
            )

        best_delta = 0.0

        for session_id in session_ids:
            if self.alternative_generator is None:
                continue

            alternatives = self.alternative_generator.generate_for_session(
                session_id=session_id,
                current_day=1,
                current_period=1,
                limit=5,
            )

            for alternative in alternatives:
                delta = getattr(alternative.estimated_score, "delta", 0.0)
                best_delta = max(best_delta, delta)

        return CourseOptimizationResult(
            course_id=course_id,
            analyzed_sessions=analyzed,
            best_delta=best_delta,
            summary=f"Analizadas {analyzed} sesiones del curso {course_id}.",
        )