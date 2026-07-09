from __future__ import annotations


class AlternativeRanker:
    """
    Ordena alternativas según su calidad estimada.
    """

    def rank(self, alternatives, limit=None):
        ranked = sorted(
            alternatives,
            key=lambda alternative: (
                getattr(alternative.estimated_score, "delta", 0),
                -getattr(alternative.estimated_score, "conflicts", 0),
            ),
            reverse=True,
        )

        if limit is not None:
            return ranked[:limit]

        return ranked

    def best(self, alternatives):
        ranked = self.rank(alternatives)

        if not ranked:
            return None

        return ranked[0]