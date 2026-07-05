from dataclasses import dataclass

from .constraints import ConstraintEngine
from .neighbourhood import Neighbourhood
from .scorer import Scorer


@dataclass
class OptimizationResult:
    initial_score: float
    final_score: float
    iterations: int
    improved: bool
    solution: object


class Optimizer:
    def __init__(self, max_iterations: int = 50):
        self.constraints = ConstraintEngine()
        self.scorer = Scorer()
        self.neighbourhood = Neighbourhood()
        self.max_iterations = max_iterations

    def evaluate(self, solution):
        solution.conflicts = self.constraints.evaluate(solution)
        self.scorer.evaluate(solution)
        return solution

    def optimize(self, solution):
        current = self.evaluate(solution.copy())
        initial_score = current.score
        iterations = 0
        improved = True

        while improved and iterations < self.max_iterations:
            improved = False
            best = current

            for candidate in self.neighbourhood.neighbours(current):
                iterations += 1
                candidate = self.evaluate(candidate)

                if candidate.score > best.score:
                    best = candidate
                    improved = True

                if iterations >= self.max_iterations:
                    break

            current = best

        return OptimizationResult(
            initial_score=initial_score,
            final_score=current.score,
            iterations=iterations,
            improved=current.score > initial_score,
            solution=current,
        )
