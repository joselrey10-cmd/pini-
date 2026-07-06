from .candidate_generator import CandidateGenerator
from .comparator import SolutionComparator


class CandidateGenerationReport:
    def build(self, base_solution, count: int = 10, swaps_per_candidate: int = 3, seed: int | None = 42) -> dict:
        result = CandidateGenerator(seed=seed).generate(
            base_solution,
            count=count,
            swaps_per_candidate=swaps_per_candidate,
        )
        comparison = SolutionComparator().compare(result.candidates)

        return {
            "generated": len(result.candidates),
            "best_name": result.best_name,
            "best_score": result.best_score,
            "ranking": [
                {
                    "rank": item.rank,
                    "name": item.name,
                    "score": item.score,
                    "conflicts": item.conflicts,
                    "sessions": item.sessions,
                }
                for item in comparison.items
            ],
        }
