from dataclasses import dataclass
import random

from .comparator import SolutionComparator


@dataclass(frozen=True)
class CandidateGenerationResult:
    candidates: dict[str, object]
    best_name: str
    best_solution: object
    best_score: float


class CandidateGenerator:
    def __init__(self, seed: int | None = None):
        self.random = random.Random(seed)
        self.comparator = SolutionComparator()

    def generate(self, base_solution, count: int = 10, swaps_per_candidate: int = 3) -> CandidateGenerationResult:
        candidates = {"base": base_solution.copy()}

        for index in range(1, max(1, count)):
            candidate = base_solution.copy()
            for _ in range(swaps_per_candidate):
                candidate = self._mutate(candidate)
            candidates[f"candidato {index}"] = candidate

        comparison = self.comparator.compare(candidates)
        best_solution = candidates[comparison.best_name] if comparison.best_name else base_solution.copy()

        return CandidateGenerationResult(
            candidates=candidates,
            best_name=comparison.best_name,
            best_solution=best_solution,
            best_score=comparison.best_score,
        )

    def _mutate(self, solution):
        if len(solution.sessions) < 2:
            return solution.copy()
        first, second = self.random.sample(range(len(solution.sessions)), 2)
        return solution.with_swapped_sessions(first, second)
