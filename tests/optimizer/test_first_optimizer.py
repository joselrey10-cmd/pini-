from packages.optimizer.models import Session
from packages.optimizer.solution import Solution
from packages.optimizer.optimizer import Optimizer


def test_optimizer_returns_result():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Ana", "2A", "Mate", "A2", 1, 1),
            Session("Luis", "1A", "Mate", "A1", 1, 2),
        ]
    )

    result = Optimizer(max_iterations=10).optimize(solution)

    assert result.initial_score <= 100
    assert result.final_score <= 100
    assert result.iterations >= 0
    assert result.solution is not None


def test_swap_sessions_preserves_subjects():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Luis", "2A", "Mate", "A2", 2, 3),
        ]
    )

    swapped = solution.with_swapped_sessions(0, 1)

    assert swapped.sessions[0].subject == "Lengua"
    assert swapped.sessions[0].day == 2
    assert swapped.sessions[0].period == 3
    assert swapped.sessions[1].subject == "Mate"
    assert swapped.sessions[1].day == 1
    assert swapped.sessions[1].period == 1
