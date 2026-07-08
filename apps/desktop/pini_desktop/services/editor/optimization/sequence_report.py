class SequenceOptimizationReport:
    def build(self, result) -> dict:
        return {
            "zone": result.zone.describe(),
            "has_sequences": result.has_sequences,
            "best_score": result.best.score if result.best else 0,
            "sequences": [
                {
                    "score": item.score,
                    "risk": item.risk,
                    "recommendation": item.recommendation,
                    "estimated_delta": item.sequence.estimated_delta,
                    "length": item.sequence.length,
                    "steps": [
                        {
                            "order": step.order,
                            "session_id": step.session_id,
                            "day": step.day,
                            "period": step.period,
                            "estimated_delta": step.estimated_delta,
                            "title": step.title,
                        }
                        for step in item.sequence.steps
                    ],
                }
                for item in result.sequences
            ],
        }
