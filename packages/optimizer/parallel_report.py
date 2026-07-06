from .parallel import ParallelOptimizer


class ParallelOptimizationReport:
    def build(self, base_solution, workers: int = 4, candidates_per_worker: int = 10) -> dict:
        result = ParallelOptimizer(
            workers=workers,
            candidates_per_worker=candidates_per_worker,
        ).optimize(base_solution)

        return {
            "workers": result.total_runs,
            "best_name": result.best_name,
            "best_score": result.best_score,
            "runs": [
                {
                    "name": run.name,
                    "score": run.score,
                    "sessions": len(run.solution.sessions),
                }
                for run in result.runs
            ],
        }
