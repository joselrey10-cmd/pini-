from dataclasses import dataclass

from .optimizer import Optimizer
from .report import QualityReport


@dataclass(frozen=True)
class SolutionComparisonItem:
    name: str
    score: float
    conflicts: int
    sessions: int
    rank: int = 0


@dataclass(frozen=True)
class SolutionComparisonResult:
    items: tuple[SolutionComparisonItem, ...]
    best_name: str
    best_score: float

    @property
    def has_winner(self) -> bool:
        return bool(self.best_name)


class SolutionComparator:
    def __init__(self):
        self.optimizer = Optimizer(max_iterations=0)

    def compare(self, named_solutions: dict[str, object]) -> SolutionComparisonResult:
        items = []

        for name, solution in named_solutions.items():
            evaluated = self.optimizer.evaluate(solution.copy())
            items.append(
                SolutionComparisonItem(
                    name=name,
                    score=evaluated.score,
                    conflicts=len(evaluated.conflicts),
                    sessions=len(evaluated.sessions),
                )
            )

        ordered = sorted(items, key=lambda item: item.score, reverse=True)
        ranked = tuple(
            SolutionComparisonItem(
                name=item.name,
                score=item.score,
                conflicts=item.conflicts,
                sessions=item.sessions,
                rank=index + 1,
            )
            for index, item in enumerate(ordered)
        )

        if not ranked:
            return SolutionComparisonResult(items=(), best_name="", best_score=0)

        return SolutionComparisonResult(
            items=ranked,
            best_name=ranked[0].name,
            best_score=ranked[0].score,
        )
