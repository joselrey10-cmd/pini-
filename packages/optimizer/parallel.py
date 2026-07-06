from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

from .candidate_generator import CandidateGenerator
from .comparator import SolutionComparator


@dataclass(frozen=True)
class ParallelOptimizationRun:
    name: str
    score: float
    solution: object


@dataclass(frozen=True)
class ParallelOptimizationResult:
    runs: tuple[ParallelOptimizationRun, ...]
    best_name: str
    best_score: float
    best_solution: object

    @property
    def total_runs(self) -> int:
        return len(self.runs)


class ParallelOptimizer:
    def __init__(self, workers: int = 4, candidates_per_worker: int = 10, swaps_per_candidate: int = 3):
        self.workers = max(1, workers)
        self.candidates_per_worker = max(1, candidates_per_worker)
        self.swaps_per_candidate = max(1, swaps_per_candidate)

    def optimize(self, base_solution) -> ParallelOptimizationResult:
        runs = []

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = {
                executor.submit(self._run_worker, base_solution, index): index
                for index in range(self.workers)
            }

            for future in as_completed(futures):
                runs.append(future.result())

        named = {run.name: run.solution for run in runs}
        comparison = SolutionComparator().compare(named)
        best_solution = named[comparison.best_name] if comparison.best_name else base_solution.copy()

        return ParallelOptimizationResult(
            runs=tuple(sorted(runs, key=lambda item: item.name)),
            best_name=comparison.best_name,
            best_score=comparison.best_score,
            best_solution=best_solution,
        )

    def _run_worker(self, base_solution, index: int) -> ParallelOptimizationRun:
        result = CandidateGenerator(seed=index + 1).generate(
            base_solution,
            count=self.candidates_per_worker,
            swaps_per_candidate=self.swaps_per_candidate,
        )
        return ParallelOptimizationRun(
            name=f"worker-{index + 1}",
            score=result.best_score,
            solution=result.best_solution,
        )
