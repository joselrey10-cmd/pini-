from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationDecision:
    accepted: bool
    reason: str
    warnings: tuple[str, ...] = ()


class SimulationDecisionEngine:
    def decide(self, comparison) -> SimulationDecision:
        warnings = []

        if comparison.room_conflicts_delta > 0:
            return SimulationDecision(
                accepted=False,
                reason="Rechazada: introduce nuevos conflictos de aula.",
                warnings=("Aumentan los conflictos de aula.",),
            )

        if comparison.teacher_gaps_delta > 0:
            warnings.append("Aumentan las ventanas del profesorado.")

        if comparison.course_gaps_delta > 0:
            warnings.append("Aumentan los huecos de cursos.")

        if comparison.delta_score > 0:
            return SimulationDecision(
                accepted=True,
                reason="Aceptada: mejora el score global sin conflictos críticos.",
                warnings=tuple(warnings),
            )

        return SimulationDecision(
            accepted=False,
            reason="Rechazada: no mejora el score global.",
            warnings=tuple(warnings),
        )


class DecisionEngine:
    def decide(self, comparison):
        return SimulationDecisionEngine().decide(comparison)