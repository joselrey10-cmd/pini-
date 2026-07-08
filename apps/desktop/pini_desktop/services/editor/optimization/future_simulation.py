from dataclasses import dataclass

from pini_desktop.services.editor.optimization.move_sequence import MoveSequence, MoveStep


@dataclass(frozen=True)
class FutureSimulationImpact:
    immediate_delta: float
    future_delta: float
    final_delta: float
    risks: tuple[str, ...]
    opportunities: tuple[str, ...]


@dataclass(frozen=True)
class FutureSimulationResult:
    sequence: MoveSequence
    impact: FutureSimulationImpact

    @property
    def is_recommended(self) -> bool:
        return self.impact.final_delta > 0 and len(self.impact.risks) <= 2


class FutureSimulationEngine:
    """Simulador predictivo inicial.

    Esta versión no modifica la base de datos. Evalúa una secuencia en memoria
    usando heurísticas de riesgo futuro.
    """

    def simulate_sequence(self, sequence: MoveSequence) -> FutureSimulationResult:
        immediate = sequence.estimated_delta
        risks = []
        opportunities = []

        future_penalty = 0.0
        seen_targets = set()
        seen_sessions = set()

        for step in sequence.steps:
            target = (step.day, step.period)

            if target in seen_targets:
                future_penalty += 1.0
                risks.append("Varias sesiones apuntan al mismo destino horario.")
            seen_targets.add(target)

            if step.session_id in seen_sessions:
                future_penalty += 1.0
                risks.append("La misma sesión aparece más de una vez en la cadena.")
            seen_sessions.add(step.session_id)

            if step.period >= 6:
                future_penalty += 0.4
                risks.append("Algún movimiento termina en última hora.")

            if step.estimated_delta > 1:
                opportunities.append(f"El paso {step.order} aporta una mejora estimada relevante.")

        complexity_penalty = max(0, sequence.length - 2) * 0.25
        if complexity_penalty:
            risks.append("Cadena larga: aumenta la incertidumbre futura.")

        future_delta = round(-(future_penalty + complexity_penalty), 2)
        final_delta = round(immediate + future_delta, 2)

        if final_delta > immediate * 0.8:
            opportunities.append("El impacto futuro mantiene casi toda la mejora inmediata.")

        return FutureSimulationResult(
            sequence=sequence,
            impact=FutureSimulationImpact(
                immediate_delta=round(immediate, 2),
                future_delta=future_delta,
                final_delta=final_delta,
                risks=tuple(dict.fromkeys(risks)),
                opportunities=tuple(dict.fromkeys(opportunities)),
            ),
        )
