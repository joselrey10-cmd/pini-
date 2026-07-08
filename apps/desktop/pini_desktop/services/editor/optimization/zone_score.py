from dataclasses import dataclass

@dataclass(frozen=True)
class ZoneScore:
    sessions: int
    gaps: int
    last_periods: int
    score: float

class ZoneScoreCalculator:
    def calculate(self, sessions) -> ZoneScore:
        sessions = tuple(sessions)
        gaps = self._count_gaps(sessions)
        last_periods = sum(1 for item in sessions if item.period >= 6)
        score = max(0.0, min(100.0, 100.0 - gaps * 4 - last_periods * 2))
        return ZoneScore(len(sessions), gaps, last_periods, round(score, 2))

    def _count_gaps(self, sessions) -> int:
        by_day = {}
        for item in sessions:
            by_day.setdefault(item.day, []).append(item.period)
        gaps = 0
        for periods in by_day.values():
            ordered = sorted(set(periods))
            for first, second in zip(ordered, ordered[1:]):
                gaps += max(0, second - first - 1)
        return gaps
