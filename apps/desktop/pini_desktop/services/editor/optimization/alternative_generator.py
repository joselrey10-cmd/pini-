from dataclasses import dataclass

from pini_desktop.services.editor.optimization.alternative_ranker import AlternativeRanker
from pini_desktop.services.editor.optimization.candidate_builder import CandidateBuilder, MoveCandidate
from pini_desktop.services.editor.optimization.explanation_builder import AlternativeExplanation, ExplanationBuilder
from pini_desktop.services.editor.optimization.score_estimator import ScoreEstimator


@dataclass(frozen=True)
class EditorAlternative:
    title: str
    estimated_delta: float
    explanation: str
    candidate: MoveCandidate
    estimated_score: float = 0.0
    reasons: tuple[str, ...] = ()
    bullets: tuple[str, ...] = ()


class AlternativeGenerator:
    def __init__(
        self,
        candidate_builder: CandidateBuilder | None = None,
        score_estimator: ScoreEstimator | None = None,
        ranker: AlternativeRanker | None = None,
        explanation_builder: ExplanationBuilder | None = None,
    ):
        self.candidate_builder = candidate_builder or CandidateBuilder()
        self.score_estimator = score_estimator or ScoreEstimator()
        self.ranker = ranker or AlternativeRanker()
        self.explanation_builder = explanation_builder or ExplanationBuilder()

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

        alternatives = []
        for candidate in candidates:
            estimated = self.score_estimator.estimate(
                candidate,
                current_day=current_day,
                current_period=current_period,
                current_score=current_score,
            )
            explanation = self.explanation_builder.build(estimated)
            alternatives.append(
                EditorAlternative(
                    title=candidate.title,
                    estimated_delta=estimated.delta,
                    estimated_score=estimated.estimated_score,
                    explanation=explanation.summary,
                    candidate=candidate,
                    reasons=estimated.reasons,
                    bullets=explanation.bullets,
                )
            )

        return self.ranker.rank(alternatives, limit=limit)
