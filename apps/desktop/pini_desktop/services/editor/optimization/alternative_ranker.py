class AlternativeRanker:
    """Ordena alternativas y elimina duplicados por destino."""

    def rank(self, alternatives, limit: int = 5):
        seen = set()
        unique = []

        for alternative in alternatives:
            candidate = alternative.candidate
            key = (candidate.session_id, candidate.day, candidate.period)
            if key in seen:
                continue
            seen.add(key)
            unique.append(alternative)

        unique.sort(
            key=lambda item: (
                item.estimated_delta,
                item.estimated_score,
            ),
            reverse=True,
        )

        return tuple(unique[:limit])
