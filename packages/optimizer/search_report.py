from .local_search import HillClimbingOptimizer


class SearchReport:
    def build(self, solution, max_iterations: int = 500):
        result = HillClimbingOptimizer(max_iterations=max_iterations).optimize(solution)
        return {
            "initial_score": result.initial_score,
            "final_score": result.final_score,
            "improved": result.improved,
            "iterations": result.iterations,
            "accepted_moves": result.accepted_moves,
            "sessions": len(result.solution.sessions),
        }
