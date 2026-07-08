from dataclasses import dataclass

from pini_desktop.services.editor.optimization.move_sequence import MoveSequence


@dataclass(frozen=True)
class SequenceScore:
    sequence: MoveSequence
    score: float
    risk: float
    recommendation: str


class ChainEvaluator:
    """Evalúa secuencias de movimientos.

    Score = mejora acumulada menos una pequeña penalización por complejidad.
    """

    def evaluate(self, sequence: MoveSequence) -> SequenceScore:
        complexity_penalty = max(0, sequence.length - 1) * 0.15
        risk = round(sequence.length * 0.1 + complexity_penalty, 2)
        score = round(sequence.estimated_delta - complexity_penalty, 2)

        if score >= 3:
            recommendation = "Cadena muy recomendable."
        elif score > 0:
            recommendation = "Cadena positiva."
        else:
            recommendation = "Cadena poco recomendable."

        return SequenceScore(
            sequence=sequence,
            score=score,
            risk=risk,
            recommendation=recommendation,
        )
