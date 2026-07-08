from dataclasses import dataclass


@dataclass(frozen=True)
class RankedAlternative:
    day: int
    period: int
    score: float
    reasons: tuple[str, ...] = ()


class AlternativeRanker:
    def rank(self, alternatives, limit: int = 5):
        ranked = sorted(
            alternatives,
            key=lambda item: getattr(item, "score", getattr(item, "delta", 0)),
            reverse=True,
        )
        return ranked[:limit]