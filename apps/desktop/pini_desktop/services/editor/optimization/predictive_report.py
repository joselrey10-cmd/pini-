class PredictiveSimulationReport:
    def build(self, predictive_score) -> dict:
        impact = predictive_score.simulation.impact
        return {
            "predictive_score": predictive_score.predictive_score,
            "recommendation": predictive_score.recommendation,
            "immediate_delta": impact.immediate_delta,
            "future_delta": impact.future_delta,
            "final_delta": impact.final_delta,
            "risks": list(impact.risks),
            "opportunities": list(impact.opportunities),
            "steps": [
                {
                    "order": step.order,
                    "session_id": step.session_id,
                    "day": step.day,
                    "period": step.period,
                    "estimated_delta": step.estimated_delta,
                    "title": step.title,
                }
                for step in predictive_score.simulation.sequence.steps
            ],
        }

    def build_text(self, predictive_score) -> str:
        data = self.build(predictive_score)
        lines = [
            "Simulación predictiva",
            "",
            f"Score predictivo: {data['predictive_score']}",
            f"Recomendación: {data['recommendation']}",
            "",
            f"Mejora inmediata: +{data['immediate_delta']}",
            f"Impacto futuro: {data['future_delta']}",
            f"Resultado final estimado: {data['final_delta']}",
            "",
            "Riesgos:",
        ]
        lines.extend(f"• {item}" for item in data["risks"] or ["Sin riesgos relevantes."])
        lines.append("")
        lines.append("Oportunidades:")
        lines.extend(f"• {item}" for item in data["opportunities"] or ["Sin oportunidades destacadas."])
        lines.append("")
        lines.append("Pasos:")
        for step in data["steps"]:
            lines.append(
                f"{step['order']}. {step['title']} · sesión {step['session_id']} "
                f"→ día {step['day']}, periodo {step['period']} · +{step['estimated_delta']}"
            )
        return "\n".join(lines)
