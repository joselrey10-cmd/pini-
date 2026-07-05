from dataclasses import dataclass

from .optimizer import Optimizer


@dataclass
class LocalSearchResult:
    initial_score: float
    final_score: float
    iterations: int
    accepted_moves: int
    solution: object

    @property
    def improved(self) -> bool:
        return self.final_score > self.initial_score


class HillClimbingOptimizer:
    """Búsqueda local básica por mejora estricta.

    Recorre vecinos y acepta solo movimientos que mejoran la puntuación.
    """

    def __init__(self, max_iterations: int = 500, max_neighbours: int = 200):
        self.max_iterations = max_iterations
        self.max_neighbours = max_neighbours
        self.optimizer = Optimizer(max_iterations=0)

    def optimize(self, solution):
        current = self.optimizer.evaluate(solution.copy())
        initial_score = current.score
        iterations = 0
        accepted = 0

        while iterations < self.max_iterations:
            best = current
            improved = False

            for candidate in self.optimizer.neighbourhood.neighbours(current, self.max_neighbours):
                iterations += 1
                candidate = self.optimizer.evaluate(candidate)

                if candidate.score > best.score:
                    best = candidate
                    improved = True

                if iterations >= self.max_iterations:
                    break

            if not improved:
                break

            current = best
            accepted += 1

        return LocalSearchResult(
            initial_score=initial_score,
            final_score=current.score,
            iterations=iterations,
            accepted_moves=accepted,
            solution=current,
        )
