class IterativeZoneSearchReport:
    def build(self, result) -> dict:
        return {
            "zone": result.zone.describe(),
            "iterations": result.iterations,
            "accumulated_delta": result.accumulated_delta,
            "has_improvement": result.has_improvement,
            "steps": [
                {
                    "iteration": step.iteration,
                    "session_id": step.suggestion.session_id,
                    "day": step.suggestion.day,
                    "period": step.suggestion.period,
                    "estimated_delta": step.suggestion.estimated_delta,
                    "accumulated_delta": step.accumulated_delta,
                    "title": step.suggestion.title,
                }
                for step in result.steps
            ],
        }
