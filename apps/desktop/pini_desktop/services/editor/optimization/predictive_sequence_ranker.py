class PredictiveSequenceRanker:
    """Ordena cadenas usando score predictivo, no solo mejora inmediata."""

    def rank(self, predictive_scores, limit: int = 5):
        ordered = sorted(
            predictive_scores,
            key=lambda item: (
                item.predictive_score,
                item.simulation.impact.final_delta,
                -len(item.simulation.impact.risks),
            ),
            reverse=True,
        )
        return tuple(ordered[:limit])
