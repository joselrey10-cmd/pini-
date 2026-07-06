from dataclasses import dataclass

from .engine import OptimizationEngine


@dataclass(frozen=True)
class ExplanationItem:
    objective: str
    before: float
    after: float
    delta: float
    message: str


@dataclass(frozen=True)
class OptimizationExplanation:
    before_score: float
    after_score: float
    improvement: float
    summary: str
    items: tuple[ExplanationItem, ...]


class OptimizationExplainer:
    def __init__(self):
        self.engine = OptimizationEngine()

    def explain(self, before_solution, after_solution) -> OptimizationExplanation:
        before = self.engine.evaluate(before_solution)
        after = self.engine.evaluate(after_solution)

        before_map = {
            item["name"]: item
            for item in before.details.get("objectives", [])
        }
        after_map = {
            item["name"]: item
            for item in after.details.get("objectives", [])
        }

        items = []
        for name, after_item in after_map.items():
            before_item = before_map.get(name, {"value": 0})
            before_value = float(before_item.get("value", 0))
            after_value = float(after_item.get("value", 0))
            delta = round(after_value - before_value, 2)

            items.append(
                ExplanationItem(
                    objective=name,
                    before=before_value,
                    after=after_value,
                    delta=delta,
                    message=self._message(name, delta),
                )
            )

        improvement = round(after.score - before.score, 2)

        return OptimizationExplanation(
            before_score=before.score,
            after_score=after.score,
            improvement=improvement,
            summary=self._summary(improvement),
            items=tuple(items),
        )

    def _summary(self, improvement: float) -> str:
        if improvement > 0:
            return f"La nueva solución mejora {improvement} puntos respecto a la anterior."
        if improvement < 0:
            return f"La nueva solución empeora {abs(improvement)} puntos respecto a la anterior."
        return "La nueva solución mantiene la misma puntuación global."

    def _message(self, objective: str, delta: float) -> str:
        labels = {
            "constraints": "restricciones",
            "teacher_compactness": "horario del profesorado",
            "student_distribution": "distribución del alumnado",
            "room_quality": "uso de aulas",
        }
        label = labels.get(objective, objective)

        if delta > 0:
            return f"Mejora en {label}: +{delta}."
        if delta < 0:
            return f"Empeora en {label}: {delta}."
        return f"Sin cambios en {label}."
