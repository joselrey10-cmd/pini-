from .genetic import GeneticOptimizer
from .local_search import HillClimbingOptimizer
from .simulated_annealing import SimulatedAnnealingOptimizer
from .tabu_search import TabuSearchOptimizer


class SearchReport:
    def build(self, solution, max_iterations: int = 500, mode: str = "hill_climbing"):
        if mode == "annealing":
            result = SimulatedAnnealingOptimizer(max_iterations=max_iterations, seed=42).optimize(solution)
            return {
                "mode": "annealing",
                "initial_score": result.initial_score,
                "final_score": result.final_score,
                "best_score": result.best_score,
                "improved": result.improved,
                "iterations": result.iterations,
                "accepted_moves": result.accepted_moves,
                "worse_moves": result.worse_moves,
                "tabu_skips": 0,
                "generations": 0,
                "mutations": 0,
                "sessions": len(result.solution.sessions),
            }

        if mode == "tabu":
            result = TabuSearchOptimizer(max_iterations=max_iterations).optimize(solution)
            return {
                "mode": "tabu",
                "initial_score": result.initial_score,
                "final_score": result.final_score,
                "best_score": result.best_score,
                "improved": result.improved,
                "iterations": result.iterations,
                "accepted_moves": result.accepted_moves,
                "worse_moves": 0,
                "tabu_skips": result.tabu_skips,
                "generations": 0,
                "mutations": 0,
                "sessions": len(result.solution.sessions),
            }

        if mode == "genetic":
            result = GeneticOptimizer(generations=max(1, max_iterations // 10), seed=42).optimize(solution)
            return {
                "mode": "genetic",
                "initial_score": result.initial_score,
                "final_score": result.final_score,
                "best_score": result.best_score,
                "improved": result.improved,
                "iterations": 0,
                "accepted_moves": 0,
                "worse_moves": 0,
                "tabu_skips": 0,
                "generations": result.generations,
                "mutations": result.mutations,
                "sessions": len(result.solution.sessions),
            }

        result = HillClimbingOptimizer(max_iterations=max_iterations).optimize(solution)
        return {
            "mode": "hill_climbing",
            "initial_score": result.initial_score,
            "final_score": result.final_score,
            "best_score": result.final_score,
            "improved": result.improved,
            "iterations": result.iterations,
            "accepted_moves": result.accepted_moves,
            "worse_moves": 0,
            "tabu_skips": 0,
            "generations": 0,
            "mutations": 0,
            "sessions": len(result.solution.sessions),
        }
