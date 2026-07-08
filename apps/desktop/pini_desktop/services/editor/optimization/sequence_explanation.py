from dataclasses import dataclass


@dataclass(frozen=True)
class SequenceExplanation:
    summary: str
    strengths: tuple[str, ...]
    risks: tuple[str, ...]
    recommendation: str


class SequenceExplanationBuilder:
    def build(self, sequence_score) -> SequenceExplanation:
        length = sequence_score.sequence.length
        delta = sequence_score.sequence.estimated_delta
        risk = sequence_score.risk

        strengths = []
        risks = []

        if delta >= 3:
            strengths.append("Mejora acumulada alta.")
        elif delta > 0:
            strengths.append("Mejora acumulada positiva.")

        if length > 1:
            strengths.append("Coordina varios movimientos que pueden mejorar la zona completa.")
        else:
            strengths.append("Movimiento simple y fácil de revisar.")

        if risk >= 0.5:
            risks.append("Cadena con varios pasos: conviene revisarla antes de aplicar.")
        if length >= 4:
            risks.append("Secuencia larga: puede afectar a varias sesiones relacionadas.")
        if not risks:
            risks.append("Riesgo bajo según la estimación inicial.")

        if delta >= 3 and risk < 0.7:
            recommendation = "Aplicar si las sesiones propuestas encajan con los criterios del centro."
        elif delta > 0:
            recommendation = "Revisar y aplicar si el impacto visual es correcto."
        else:
            recommendation = "No se recomienda aplicar esta cadena."

        summary = f"Cadena de {length} movimiento(s), mejora estimada +{delta} y riesgo {risk}."

        return SequenceExplanation(
            summary=summary,
            strengths=tuple(strengths),
            risks=tuple(risks),
            recommendation=recommendation,
        )
