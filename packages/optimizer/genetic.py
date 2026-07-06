from dataclasses import dataclass
import random

from .optimizer import Optimizer


@dataclass
class GeneticResult:
    initial_score: float
    final_score: float
    best_score: float
    generations: int
    population_size: int
    mutations: int
    solution: object

    @property
    def improved(self) -> bool:
        return self.best_score > self.initial_score


class GeneticOptimizer:
    """Optimizador genético inicial.

    Crea una población a partir de variaciones de la solución original,
    selecciona las mejores, cruza sesiones y aplica mutaciones simples.
    """

    def __init__(
        self,
        generations: int = 30,
        population_size: int = 20,
        elite_size: int = 4,
        mutation_rate: float = 0.20,
        seed: int | None = None,
    ):
        self.generations = generations
        self.population_size = max(4, population_size)
        self.elite_size = max(1, min(elite_size, self.population_size))
        self.mutation_rate = mutation_rate
        self.random = random.Random(seed)
        self.optimizer = Optimizer(max_iterations=0)

    def optimize(self, solution):
        base = self.optimizer.evaluate(solution.copy())
        initial_score = base.score

        population = self._initial_population(base)
        mutations = 0

        best = max(population, key=lambda item: item.score).copy()

        for _generation in range(self.generations):
            population = [self.optimizer.evaluate(item) for item in population]
            population.sort(key=lambda item: item.score, reverse=True)

            if population[0].score > best.score:
                best = population[0].copy()

            next_population = [item.copy() for item in population[: self.elite_size]]

            while len(next_population) < self.population_size:
                parent_a = self._select_parent(population)
                parent_b = self._select_parent(population)
                child = self._crossover(parent_a, parent_b)

                if self.random.random() < self.mutation_rate:
                    child = self._mutate(child)
                    mutations += 1

                next_population.append(self.optimizer.evaluate(child))

            population = next_population

        final_best = max(population + [best], key=lambda item: item.score)

        return GeneticResult(
            initial_score=initial_score,
            final_score=final_best.score,
            best_score=final_best.score,
            generations=self.generations,
            population_size=self.population_size,
            mutations=mutations,
            solution=final_best,
        )

    def _initial_population(self, base_solution):
        population = [base_solution.copy()]
        while len(population) < self.population_size:
            candidate = base_solution.copy()
            swaps = self.random.randint(1, max(1, len(candidate.sessions) // 2))
            for _ in range(swaps):
                candidate = self._mutate(candidate)
            population.append(self.optimizer.evaluate(candidate))
        return population

    def _select_parent(self, population):
        sample_size = min(3, len(population))
        sample = self.random.sample(population, sample_size)
        return max(sample, key=lambda item: item.score)

    def _crossover(self, parent_a, parent_b):
        if not parent_a.sessions or len(parent_a.sessions) != len(parent_b.sessions):
            return parent_a.copy()

        child = parent_a.copy()
        split = self.random.randint(0, len(child.sessions) - 1)
        child.sessions = parent_a.sessions[:split] + parent_b.sessions[split:]
        return child

    def _mutate(self, solution):
        if len(solution.sessions) < 2:
            return solution.copy()

        first, second = self.random.sample(range(len(solution.sessions)), 2)
        return solution.with_swapped_sessions(first, second)
