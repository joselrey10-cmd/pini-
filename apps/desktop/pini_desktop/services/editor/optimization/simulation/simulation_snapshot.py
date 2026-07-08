from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from .global_metrics import GlobalMetrics, GlobalMetricsCalculator
from .virtual_schedule import VirtualSchedule, VirtualSession


@dataclass(frozen=True)
class SimulationSnapshot:
    id: str
    created_at: str
    sessions: tuple[VirtualSession, ...]
    metrics: GlobalMetrics
    label: str = ""

    @classmethod
    def capture(
        cls,
        schedule: VirtualSchedule,
        label: str = "",
        calculator: GlobalMetricsCalculator | None = None,
    ) -> "SimulationSnapshot":
        calculator = calculator or GlobalMetricsCalculator()
        return cls(
            id=str(uuid4()),
            created_at=datetime.now().isoformat(timespec="seconds"),
            sessions=schedule.sessions(),
            metrics=calculator.calculate(schedule),
            label=label,
        )
