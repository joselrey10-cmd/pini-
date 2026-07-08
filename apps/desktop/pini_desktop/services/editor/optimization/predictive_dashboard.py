from dataclasses import dataclass


@dataclass(frozen=True)
class PredictiveDashboardItem:
    rank: int
    title: str
    immediate_delta: float
    future_delta: float
    final_delta: float
    predictive_score: float
    risks_count: int
    opportunities_count: int
    recommendation: str


@dataclass(frozen=True)
class PredictiveDashboard:
    items: tuple[PredictiveDashboardItem, ...]

    @property
    def best(self):
        return self.items[0] if self.items else None

    @property
    def has_items(self) -> bool:
        return bool(self.items)


class PredictiveDashboardBuilder:
    def build(self, predictive_scores) -> PredictiveDashboard:
        ordered = sorted(
            predictive_scores,
            key=lambda item: (
                item.predictive_score,
                item.simulation.impact.final_delta,
                -len(item.simulation.impact.risks),
            ),
            reverse=True,
        )

        items = []
        for index, item in enumerate(ordered, start=1):
            impact = item.simulation.impact
            title = self._title(item)
            items.append(
                PredictiveDashboardItem(
                    rank=index,
                    title=title,
                    immediate_delta=impact.immediate_delta,
                    future_delta=impact.future_delta,
                    final_delta=impact.final_delta,
                    predictive_score=item.predictive_score,
                    risks_count=len(impact.risks),
                    opportunities_count=len(impact.opportunities),
                    recommendation=item.recommendation,
                )
            )

        return PredictiveDashboard(items=tuple(items))

    def _title(self, predictive_score) -> str:
        steps = predictive_score.simulation.sequence.steps
        if not steps:
            return "Cadena sin pasos"
        if len(steps) == 1:
            return steps[0].title or f"Movimiento sesión {steps[0].session_id}"
        return f"Cadena de {len(steps)} movimientos"
