from pini_desktop.services.editor.optimization.alternative_comparator import AlternativeComparator


class AlternativeComparisonReport:
    def build(self, alternatives) -> dict:
        comparison = AlternativeComparator().compare(alternatives)

        return {
            "has_best": comparison.has_best,
            "best_title": comparison.best.alternative.title if comparison.best else "",
            "best_delta": comparison.best.alternative.estimated_delta if comparison.best else 0,
            "items": [
                {
                    "rank": item.rank,
                    "title": item.alternative.title,
                    "delta": item.alternative.estimated_delta,
                    "score": item.alternative.estimated_score,
                    "recommendation": item.recommendation,
                    "strengths": list(item.strengths),
                    "weaknesses": list(item.weaknesses),
                }
                for item in comparison.items
            ],
        }
