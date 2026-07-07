from dataclasses import dataclass

from pini_desktop.services.editor.optimization.candidate_builder import MoveCandidate


@dataclass(frozen=True)
class EstimatedScore:
    candidate: MoveCandidate
    current_score: float
    estimated_score: float
    delta: float
    reasons: tuple[str, ...] = ()


class ScoreEstimator:
    """Estimador rápido de mejora.

    No sustituye al score real del optimizador. Sirve para ordenar alternativas
    de forma ligera antes de hacer cálculos más costosos.
    """

    def estimate(
        self,
        candidate: MoveCandidate,
        current_day: int,
        current_period: int,
        current_score: float = 80.0,
    ) -> EstimatedScore:
        distance = abs(candidate.day - current_day) + abs(candidate.period - current_period)

        # Heurística inicial:
        # - movimientos cercanos tienen menos riesgo;
        # - evitar últimos periodos suma algo;
        # - repartir a días distintos suma algo.
        delta = 0.0
        reasons = []

        if distance <= 1:
            delta += 1.0
            reasons.append("Movimiento cercano y de bajo riesgo.")
        elif distance <= 2:
            delta += 0.6
            reasons.append("Movimiento moderado dentro de la zona afectada.")
        else:
            delta += 0.2
            reasons.append("Movimiento más alejado, requiere revisión.")

        if candidate.period < current_period:
            delta += 0.4
            reasons.append("Adelanta la sesión en la jornada.")

        if candidate.day != current_day:
            delta += 0.3
            reasons.append("Mejora el reparto entre días.")

        if candidate.period >= 6:
            delta -= 0.3
            reasons.append("Penalización por última hora.")

        estimated_score = max(0.0, min(100.0, current_score + delta))

        return EstimatedScore(
            candidate=candidate,
            current_score=round(current_score, 2),
            estimated_score=round(estimated_score, 2),
            delta=round(estimated_score - current_score, 2),
            reasons=tuple(reasons),
        )
