from .optimizer import Optimizer


class QualityReport:
    def build(self, solution):
        evaluated = Optimizer(max_iterations=0).evaluate(solution)
        return {
            "score": evaluated.score,
            "conflicts": list(evaluated.conflicts),
            "sessions": len(evaluated.sessions),
        }
