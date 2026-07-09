from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from .global_metrics import GlobalMetrics, GlobalMetricsCalculator


@dataclass(frozen=True)
class SimulationSnapshot:
    id: str
    label: str
    created_at: str
    metrics: GlobalMetrics
    session_ids: tuple[int, ...]
    positions: dict[int, tuple[int, int]]

    @classmethod
    def create(cls, virtual_schedule, label: str = "") -> "SimulationSnapshot":
        return cls.from_virtual_schedule(virtual_schedule, label=label)

    @classmethod
    def from_virtual_schedule(cls, virtual_schedule, label: str = "") -> "SimulationSnapshot":
        sessions = tuple(virtual_schedule.sessions())
        metrics = GlobalMetricsCalculator().calculate(virtual_schedule)
        return cls(
            id=str(uuid4()),
            label=label or "snapshot",
            created_at=datetime.now().isoformat(timespec="seconds"),
            metrics=metrics,
            session_ids=tuple(session.id for session in sessions),
            positions={session.id: (session.day, session.period) for session in sessions},
        )
