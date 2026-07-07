from dataclasses import dataclass

from pini_desktop.services.editor.optimization.candidate_builder import CandidateBuilder, MoveCandidate


@dataclass(frozen=True)
class EditorAlternative:
    title: str
    estimated_delta: float
    explanation: str
    candidate: MoveCandidate


class AlternativeGenerator:
    """Generador inicial de alternativas.

    De momento usa CandidateBuilder y asigna una mejora estimada básica para
    permitir construir la UI y los tests antes de incorporar scoring real.
    """

    def __init__(self, candidate_builder: CandidateBuilder | None = None):
        self.candidate_builder = candidate_builder or CandidateBuilder()

    def generate_for_session(
        self,
        session_id: int,
        current_day: int,
        current_period: int,
        limit: int = 5,
    ) -> tuple[EditorAlternative, ...]:
        candidates = self.candidate_builder.build_move_candidates(
            session_id=session_id,
            current_day=current_day,
            current_period=current_period,
        )

        alternatives = []
        for index, candidate in enumerate(candidates[:limit]):
            estimated_delta = round(max(0.1, 1.5 - index * 0.2), 2)
            alternatives.append(
                EditorAlternative(
                    title=candidate.title,
                    estimated_delta=estimated_delta,
                    explanation=candidate.reason,
                    candidate=candidate,
                )
            )

        return tuple(alternatives)
