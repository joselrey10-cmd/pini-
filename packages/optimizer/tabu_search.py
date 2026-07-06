from dataclasses import dataclass
from collections import deque

from .optimizer import Optimizer


@dataclass
class TabuSearchResult:
    initial_score: float
    final_score: float
    best_score: float
    iterations: int
    accepted_moves: int
    tabu_skips: int
    solution: object

    @property
    def improved(self) -> bool:
        return self.best_score > self.initial_score


class TabuSearchOptimizer:
    """Búsqueda tabú básica.

    Explora vecinos, evita repetir firmas recientes y acepta el mejor candidato
    no tabú, incluso si no mejora de forma inmediata.
    """

    def __init__(self, max_iterations: int = 500, tabu_size: int = 30, max_neighbours: int = 100):
        self.max_iterations = max_iterations
        self.tabu_size = tabu_size
        self.max_neighbours = max_neighbours
        self.optimizer = Optimizer(max_iterations=0)

    def optimize(self, solution):
        current = self.optimizer.evaluate(solution.copy())
        best = current.copy()
        initial_score = current.score

        tabu_list = deque(maxlen=self.tabu_size)
        tabu_list.append(self._signature(current))

        iterations = 0
        accepted_moves = 0
        tabu_skips = 0

        while iterations < self.max_iterations:
            best_candidate = None
            best_candidate_signature = None

            for candidate in self.optimizer.neighbourhood.neighbours(current, self.max_neighbours):
                iterations += 1
                signature = self._signature(candidate)

                if signature in tabu_list:
                    tabu_skips += 1
                    if iterations >= self.max_iterations:
                        break
                    continue

                candidate = self.optimizer.evaluate(candidate)

                if best_candidate is None or candidate.score > best_candidate.score:
                    best_candidate = candidate
                    best_candidate_signature = signature

                if iterations >= self.max_iterations:
                    break

            if best_candidate is None:
                break

            current = best_candidate
            tabu_list.append(best_candidate_signature)
            accepted_moves += 1

            if current.score > best.score:
                best = current.copy()

        return TabuSearchResult(
            initial_score=initial_score,
            final_score=current.score,
            best_score=best.score,
            iterations=iterations,
            accepted_moves=accepted_moves,
            tabu_skips=tabu_skips,
            solution=best,
        )

    def _signature(self, solution):
        return tuple(
            sorted(
                (
                    session.teacher,
                    session.course,
                    session.subject,
                    session.room,
                    session.day,
                    session.period,
                )
                for session in solution.sessions
            )
        )
