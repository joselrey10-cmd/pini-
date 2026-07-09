from dataclasses import dataclass

from pini_desktop.services.editor.optimization.move_sequence import MoveSequence, MoveStep
from pini_desktop.services.editor.optimization.simulation.decision_engine import SimulationDecisionEngine
from pini_desktop.services.editor.optimization.simulation.global_metrics import GlobalMetricsCalculator
from pini_desktop.services.editor.optimization.simulation.global_simulation_engine import GlobalSimulationEngine
from pini_desktop.services.editor.optimization.simulation.simulation_comparison import SimulationComparisonService
from pini_desktop.services.editor.optimization.simulation.simulation_snapshot import SimulationSnapshot


@dataclass(frozen=True)
class DummySession:
    id: int
    teacher_id: int
    course_id: int
    room_id: int
    day: int
    period: int

    def with_position(self, day, period):
        return DummySession(self.id, self.teacher_id, self.course_id, self.room_id, day, period)


class DummyVirtualSchedule:
    def __init__(self, sessions):
        self._sessions = {session.id: session for session in sessions}

    def sessions(self):
        return tuple(self._sessions.values())

    def clone(self):
        return DummyVirtualSchedule(self.sessions())

    def move_session(self, session_id, day, period):
        self._sessions[session_id] = self._sessions[session_id].with_position(day, period)


def test_global_metrics_detects_gaps_and_conflicts():
    schedule = DummyVirtualSchedule([
        DummySession(1, 1, 1, 1, 1, 1),
        DummySession(2, 1, 1, 1, 1, 3),
        DummySession(3, 2, 2, 1, 1, 3),
    ])

    metrics = GlobalMetricsCalculator().calculate(schedule)

    assert metrics.sessions == 3
    assert metrics.teacher_gaps == 1
    assert metrics.course_gaps == 1
    assert metrics.room_conflicts == 1
    assert metrics.score < 100


def test_snapshot_and_comparison():
    before_schedule = DummyVirtualSchedule([
        DummySession(1, 1, 1, 1, 1, 1),
        DummySession(2, 1, 1, 2, 1, 3),
    ])
    after_schedule = before_schedule.clone()
    after_schedule.move_session(2, 1, 2)

    before = SimulationSnapshot.from_virtual_schedule(before_schedule, "before")
    after = SimulationSnapshot.from_virtual_schedule(after_schedule, "after")

    comparison = SimulationComparisonService().compare(before, after)

    assert comparison.after_score >= comparison.before_score
    assert comparison.delta_score >= 0


def test_decision_engine_accepts_improvement():
    before_schedule = DummyVirtualSchedule([
        DummySession(1, 1, 1, 1, 1, 1),
        DummySession(2, 1, 1, 2, 1, 3),
    ])
    after_schedule = before_schedule.clone()
    after_schedule.move_session(2, 1, 2)

    before = SimulationSnapshot.from_virtual_schedule(before_schedule, "before")
    after = SimulationSnapshot.from_virtual_schedule(after_schedule, "after")
    comparison = SimulationComparisonService().compare(before, after)

    decision = SimulationDecisionEngine().decide(comparison)

    assert decision.accepted


def test_global_simulation_engine_runs_sequence():
    schedule = DummyVirtualSchedule([
        DummySession(1, 1, 1, 1, 1, 1),
        DummySession(2, 1, 1, 2, 1, 3),
    ])
    sequence = MoveSequence(steps=(MoveStep(1, 2, 1, 2, 1.0, "Cerrar hueco"),))

    result = GlobalSimulationEngine().simulate_sequence(schedule, sequence)

    assert result.before.label == "before"
    assert result.after.label == "after"
    assert result.decision.accepted
