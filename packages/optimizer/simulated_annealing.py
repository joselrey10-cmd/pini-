from dataclasses import dataclass
import math
import random

from .optimizer import Optimizer


@dataclass
class AnnealingResult:
    initial_score: float
    final_score: float
    best_score: float
    iterations: int
    accepted_moves: int
    worse_moves: int
    solution: object

    @property
    def improved(self) -> bool:
        return self.best_score > self.initial_score


class SimulatedAnnealingOptimizer:
    """Optimizador por recocido simulado.

    Acepta movimientos peores con una probabilidad que baja con la temperatura.
    Esto ayuda a escapar de óptimos locales.
    """

    def __init__(
        self,
        max_iterations: int = 1000,
        initial_temperature: float = 10.0,
        cooling_rate: float = 0.97,
        seed: int | None = None,
    ):
        self.max_iterations = max_iterations
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.random = random.Random(seed)
        self.optimizer = Optimizer(max_iterations=0)

    def optimize(self, solution):
        current = self.optimizer.evaluate(solution.copy())
        best = current.copy()
        initial_score = current.score

        temperature = self.initial_temperature
        iterations = 0
        accepted_moves = 0
        worse_moves = 0

        while iterations < self.max_iterations and temperature > 0.01:
            neighbours = list(self.optimizer.neighbourhood.neighbours(current, max_neighbours=50))
            if not neighbours:
                break

            candidate = self.random.choice(neighbours)
            candidate = self.optimizer.evaluate(candidate)

            delta = candidate.score - current.score
            accept = delta >= 0 or self._accept_worse(delta, temperature)

            if accept:
                if delta < 0:
                    worse_moves += 1
                current = candidate
                accepted_moves += 1

                if current.score > best.score:
                    best = current.copy()

            temperature *= self.cooling_rate
            iterations += 1

        return AnnealingResult(
            initial_score=initial_score,
            final_score=current.score,
            best_score=best.score,
            iterations=iterations,
            accepted_moves=accepted_moves,
            worse_moves=worse_moves,
            solution=best,
        )

    def _accept_worse(self, delta: float, temperature: float) -> bool:
        probability = math.exp(delta / temperature)
        return self.random.random() < probability
