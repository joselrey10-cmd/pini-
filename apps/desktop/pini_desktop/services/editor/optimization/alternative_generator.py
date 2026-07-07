from dataclasses import dataclass

from pini_desktop.services.editor.optimization.candidate_builder import CandidateBuilder, MoveCandidate
from pini_desktop.services.editor.optimization.score_estimator import ScoreEstimator


@dataclass(frozen=True)
class EditorAlternative:
    title: str
    estimated_delta: float
    explanation: str
    candidate: MoveCandidate
    estimated_score: float = 0.0
    reasons: tuple[str, ...] = ()


class AlternativeGenerator:
    def __init__(
        self,
        candidate_builder: CandidateBuilder | None = None,
        score_estimator: ScoreEstimator | None = None,
    ):
        self.candidate_builder = candidate_builder or CandidateBuilder()
        self.score_estimator = score_estimator or ScoreEstimator()

    def generate_for_session(
        self,
        session_id: int,
        current_day: int,
        current_period: int,
        limit: int = 5,
        current_score: float = 80.0,
    ) -> tuple[EditorAlternative, ...]:
        candidates = self.candidate_builder.build_move_candidates(
            session_id=session_id,
            current_day=current_day,
            current_period=current_period,
        )

        estimated = [
            self.score_estimator.estimate(
                candidate,
                current_day=current_day,
                current_period=current_period,
                current_score=current_score,
            )
            for candidate in candidates
        ]

        estimated.sort(key=lambda item: item.delta, reverse=True)

        alternatives = []
        for item in estimated[:limit]:
            explanation = " ".join(item.reasons) if item.reasons else item.candidate.reason
            alternatives.append(
                EditorAlternative(
                    title=item.candidate.title,
                    estimated_delta=item.delta,
                    estimated_score=item.estimated_score,
                    explanation=explanation,
                    candidate=item.candidate,
                    reasons=item.reasons,
                )
            )

        return tuple(alternatives)
