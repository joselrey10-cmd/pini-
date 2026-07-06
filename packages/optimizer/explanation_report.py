from .explainer import OptimizationExplainer


class OptimizationExplanationReport:
    def build(self, before_solution, after_solution) -> dict:
        explanation = OptimizationExplainer().explain(before_solution, after_solution)
        return {
            "before_score": explanation.before_score,
            "after_score": explanation.after_score,
            "improvement": explanation.improvement,
            "summary": explanation.summary,
            "items": [
                {
                    "objective": item.objective,
                    "before": item.before,
                    "after": item.after,
                    "delta": item.delta,
                    "message": item.message,
                }
                for item in explanation.items
            ],
        }
