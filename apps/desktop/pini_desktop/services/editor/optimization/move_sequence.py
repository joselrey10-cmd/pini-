from dataclasses import dataclass


@dataclass(frozen=True)
class MoveStep:
    order: int
    session_id: int
    day: int
    period: int
    estimated_delta: float
    title: str = ""


@dataclass(frozen=True)
class MoveSequence:
    steps: tuple[MoveStep, ...]

    @property
    def length(self) -> int:
        return len(self.steps)

    @property
    def estimated_delta(self) -> float:
        return round(sum(step.estimated_delta for step in self.steps), 2)

    @property
    def session_ids(self) -> tuple[int, ...]:
        return tuple(step.session_id for step in self.steps)

    def append(self, step: MoveStep) -> "MoveSequence":
        return MoveSequence(steps=self.steps + (step,))
