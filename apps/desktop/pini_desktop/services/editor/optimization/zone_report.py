class ZoneOptimizationReport:
    def build(self, result) -> dict:
        return {
            "zone": result.zone.describe(),
            "sessions": result.before.sessions,
            "gaps": result.before.gaps,
            "last_periods": result.before.last_periods,
            "score": result.before.score,
            "best_delta": result.best_delta,
            "suggestions": [
                {"session_id": s.session_id, "day": s.day, "period": s.period, "estimated_delta": s.estimated_delta, "title": s.title}
                for s in result.suggestions
            ],
        }
