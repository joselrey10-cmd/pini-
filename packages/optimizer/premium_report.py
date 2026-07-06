from .premium_optimizer import PremiumOptimizer

class PremiumOptimizationReport:
    def build(self,solution,workers=8,candidates_per_worker=100):
        r=PremiumOptimizer(workers,candidates_per_worker).optimize(solution)
        return {
            "explored":r.explored,
            "best_score":r.best_score,
            "estimated_search":"high",
            "recommendation":"Usar esta solución como horario final."
        }
