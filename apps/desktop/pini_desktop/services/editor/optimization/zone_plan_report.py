class ZoneImprovementPlanReport:
    def build(self, plan) -> dict:
        return {
            "zone": plan.zone_label,
            "estimated_delta": plan.estimated_delta,
            "actions": [
                {
                    "order": action.order,
                    "session_id": action.session_id,
                    "day": action.day,
                    "period": action.period,
                    "estimated_delta": action.estimated_delta,
                    "title": action.title,
                }
                for action in plan.actions
            ],
        }
