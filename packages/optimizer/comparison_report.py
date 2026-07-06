from .comparator import SolutionComparator


class SolutionComparisonReport:
    def build(self, named_solutions: dict[str, object]) -> dict:
        result = SolutionComparator().compare(named_solutions)
        return {
            "best_name": result.best_name,
            "best_score": result.best_score,
            "items": [
                {
                    "rank": item.rank,
                    "name": item.name,
                    "score": item.score,
                    "conflicts": item.conflicts,
                    "sessions": item.sessions,
                }
                for item in result.items
            ],
        }
