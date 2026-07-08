from pini_desktop.services.editor.optimization.predictive_dashboard import PredictiveDashboardBuilder


class PredictiveDashboardReport:
    def build(self, predictive_scores) -> dict:
        dashboard = PredictiveDashboardBuilder().build(predictive_scores)
        return {
            "has_items": dashboard.has_items,
            "best": self._item(dashboard.best) if dashboard.best else None,
            "items": [self._item(item) for item in dashboard.items],
        }

    def _item(self, item):
        return {
            "rank": item.rank,
            "title": item.title,
            "immediate_delta": item.immediate_delta,
            "future_delta": item.future_delta,
            "final_delta": item.final_delta,
            "predictive_score": item.predictive_score,
            "risks_count": item.risks_count,
            "opportunities_count": item.opportunities_count,
            "recommendation": item.recommendation,
        }

    def build_text(self, predictive_scores) -> str:
        data = self.build(predictive_scores)
        if not data["has_items"]:
            return "No hay cadenas predictivas para mostrar."

        lines = ["Resumen predictivo de cadenas", ""]
        best = data["best"]
        lines.extend([
            "Mejor cadena:",
            f"{best['title']}",
            f"Score predictivo: {best['predictive_score']}",
            f"Resultado final estimado: {best['final_delta']}",
            f"Recomendación: {best['recommendation']}",
            "",
            "Ranking:",
        ])

        for item in data["items"]:
            lines.append(
                f"#{item['rank']} · {item['title']} · inmediato +{item['immediate_delta']} · "
                f"futuro {item['future_delta']} · final {item['final_delta']} · "
                f"riesgos {item['risks_count']}"
            )

        return "\n".join(lines)
