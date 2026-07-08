from __future__ import annotations

from dataclasses import dataclass

from .simulation_comparison import SimulationComparison


@dataclass(frozen=True)
class SimulationDecision:
    accepted: bool
    reason: str
    warnings: tuple[str, ...] = ()


class DecisionEngine:
    """Basic accept/reject rules for global simulations."""

    def decide(self, comparison: SimulationComparison) -> SimulationDecision:
        warnings = []
        if comparison.adds_conflicts:
            return SimulationDecision(False, "Rechazada: introduce conflictos nuevos.")
        if comparison.teacher_gap_delta > 0:
            warnings.append("Aumentan las ventanas del profesorado.")
        if comparison.course_gap_delta > 0:
            warnings.append("Aumentan los huecos de algún curso.")
        if comparison.score_delta > 0:
            return SimulationDecision(True, "Aceptada: mejora el score global sin conflictos nuevos.", tuple(warnings))
        if comparison.score_delta == 0 and not warnings:
            return SimulationDecision(True, "Aceptada: mantiene el score global sin empeorar métricas críticas.")
        return SimulationDecision(False, "Rechazada: no mejora el score global.", tuple(warnings))
