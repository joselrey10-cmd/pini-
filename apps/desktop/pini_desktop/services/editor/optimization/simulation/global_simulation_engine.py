from __future__ import annotations

from dataclasses import dataclass

from pini_desktop.services.editor.optimization.move_sequence import MoveSequence

from .decision_engine import DecisionEngine, SimulationDecision
from .global_metrics import GlobalMetricsCalculator
from .simulation_comparison import SimulationComparison, SimulationComparisonService
from .simulation_snapshot import SimulationSnapshot
from .virtual_schedule import VirtualSchedule


@dataclass(frozen=True)
class GlobalSimulationResult:
    before: SimulationSnapshot
    after: SimulationSnapshot
    comparison: SimulationComparison
    decision: SimulationDecision
    virtual_schedule: VirtualSchedule


class GlobalSimulationEngine:
    """Runs a full-centre simulation without touching the real schedule."""

    def __init__(
        self,
        metrics_calculator: GlobalMetricsCalculator | None = None,
        comparison_service: SimulationComparisonService | None = None,
        decision_engine: DecisionEngine | None = None,
    ):
        self.metrics_calculator = metrics_calculator or GlobalMetricsCalculator()
        self.comparison_service = comparison_service or SimulationComparisonService()
        self.decision_engine = decision_engine or DecisionEngine()

    def simulate_sequence(self, schedule: VirtualSchedule | object, sequence: MoveSequence) -> GlobalSimulationResult:
        virtual = VirtualSchedule.from_schedule(schedule)
        before = SimulationSnapshot.capture(virtual, label="before", calculator=self.metrics_calculator)

        for step in sequence.steps:
            virtual.move_session(step.session_id, step.day, step.period)

        after = SimulationSnapshot.capture(virtual, label="after", calculator=self.metrics_calculator)
        comparison = self.comparison_service.compare(before, after)
        decision = self.decision_engine.decide(comparison)

        return GlobalSimulationResult(
            before=before,
            after=after,
            comparison=comparison,
            decision=decision,
            virtual_schedule=virtual,
        )
