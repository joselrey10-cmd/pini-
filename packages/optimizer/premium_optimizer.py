from dataclasses import dataclass
from .parallel import ParallelOptimizer

@dataclass(frozen=True)
class PremiumOptimizationResult:
    explored:int
    best_score:float
    best_solution:object

class PremiumOptimizer:
    def __init__(self, workers:int=8,candidates_per_worker:int=100):
        self.workers=workers
        self.candidates_per_worker=candidates_per_worker

    def optimize(self,solution):
        result=ParallelOptimizer(
            workers=self.workers,
            candidates_per_worker=self.candidates_per_worker
        ).optimize(solution)
        return PremiumOptimizationResult(
            explored=self.workers*self.candidates_per_worker,
            best_score=result.best_score,
            best_solution=result.best_solution
        )
