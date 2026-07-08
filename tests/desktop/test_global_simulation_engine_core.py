from pini_desktop.services.editor.optimization.move_sequence import MoveSequence, MoveStep
from pini_desktop.services.editor.optimization.simulation import (
    DecisionEngine,
    GlobalMetricsCalculator,
    GlobalSimulationEngine,
    SimulationComparisonService,
    SimulationSnapshot,
    VirtualSchedule,
    VirtualSession,
)


def sample_schedule():
    return VirtualSchedule.from_sessions(
        [
            VirtualSession(1, 1, 1, 10, 100, 1, 1),
            VirtualSession(2, 1, 2, 11, 101, 1, 3),
            VirtualSession(3, 2, 1, 10, 100, 2, 2),
        ]
    )


def test_virtual_schedule_move_swap_clone_and_reset():
    schedule = sample_schedule()
    clone = schedule.clone()

    schedule.move_session(1, 1, 2)
    assert schedule.get_session(1).period == 2
    assert clone.get_session(1).period == 1

    schedule.swap_sessions(1, 2)
    assert schedule.get_session(1).period == 3
    assert schedule.get_session(2).period == 2

    schedule.reset()
    assert schedule.get_session(1).period == 1
    assert len(schedule.teacher_schedule(10)) == 2
    assert len(schedule.course_schedule(1)) == 2
    assert len(schedule.room_schedule(100)) == 2


def test_global_metrics_counts_conflicts_and_gaps():
    schedule = VirtualSchedule.from_sessions(
        [
            VirtualSession(1, 1, 1, 10, 100, 1, 1),
            VirtualSession(2, 1, 2, 10, 101, 1, 1),
            VirtualSession(3, 1, 3, 11, 102, 1, 3),
        ]
    )

    metrics = GlobalMetricsCalculator().calculate(schedule)

    assert metrics.sessions == 3
    assert metrics.teacher_conflicts == 1
    assert metrics.course_conflicts == 1
    assert metrics.course_gaps >= 1
    assert metrics.score < 100


def test_snapshot_comparison_and_decision():
    schedule = sample_schedule()
    before = SimulationSnapshot.capture(schedule)
    schedule.move_session(2, 1, 2)
    after = SimulationSnapshot.capture(schedule)

    comparison = SimulationComparisonService().compare(before, after)
    decision = DecisionEngine().decide(comparison)

    assert comparison.moved_sessions == 1
    assert comparison.score_delta >= 0
    assert decision.accepted


def test_global_simulation_engine_does_not_modify_original_schedule():
    schedule = sample_schedule()
    sequence = MoveSequence(steps=(MoveStep(1, 2, 1, 2, 1.0, "Cerrar hueco"),))

    result = GlobalSimulationEngine().simulate_sequence(schedule, sequence)

    assert result.comparison.moved_sessions == 1
    assert result.decision.accepted
    assert schedule.get_session(2).period == 3
    assert result.virtual_schedule.get_session(2).period == 2
