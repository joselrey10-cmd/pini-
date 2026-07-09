from __future__ import annotations

from dataclasses import dataclass

from .decision_engine import SimulationDecision, SimulationDecisionEngine
from .simulation_comparison import SimulationComparison, SimulationComparisonService
from .simulation_snapshot import SimulationSnapshot
from .virtual_schedule import VirtualSchedule


@dataclass(frozen=True)
class GlobalSimulationResult:
    before_snapshot: SimulationSnapshot
    after_snapshot: SimulationSnapshot
    comparison: SimulationComparison
    decision: SimulationDecision
    virtual_schedule: VirtualSchedule

    @property
    def before(self) -> SimulationSnapshot:
        return self.before_snapshot

    @property
    def after(self) -> SimulationSnapshot:
        return self.after_snapshot




class GlobalSimulationEngine:
    def __init__(self, comparison_service=None, decision_engine=None):
        self.comparison_service = comparison_service or SimulationComparisonService()
        self.decision_engine = decision_engine or SimulationDecisionEngine()

    def simulate_sequence(self, schedule, sequence) -> GlobalSimulationResult:
        virtual_schedule = VirtualSchedule.from_schedule(schedule)
        before = SimulationSnapshot.create(virtual_schedule, label="before")

        for step in self._steps(sequence):
            session_id = self._value(step, ("session_id", "id"), 0)
            day = self._value(step, ("target_day", "day", "new_day"), 1)
            period = self._value(step, ("target_period", "period", "new_period"), 2)
            virtual_schedule.move_session(int(session_id), int(day), int(period))

        after = SimulationSnapshot.create(virtual_schedule, label="after")
        comparison = self.comparison_service.compare(before, after)
        decision = self.decision_engine.decide(comparison)

        return GlobalSimulationResult(
            before_snapshot=before,
            after_snapshot=after,
            comparison=comparison,
            decision=decision,
            virtual_schedule=virtual_schedule,
        )

    def simulate(self, schedule, sequence) -> GlobalSimulationResult:
        return self.simulate_sequence(schedule, sequence)

    def _steps(self, sequence):
        steps = getattr(sequence, "steps", sequence)
        if callable(steps):
            steps = steps()
        return tuple(steps)

    def _value(self, step, names: tuple[str, ...], index: int):
        for name in names:
            if hasattr(step, name):
                value = getattr(step, name)
                if value is not None:
                    return value
        try:
            return step[index]
        except Exception as exc:
            raise AttributeError(f"No se pudo leer el dato {names[0]} del paso de simulación.") from exc
