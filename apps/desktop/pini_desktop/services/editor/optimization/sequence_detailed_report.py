from pini_desktop.services.editor.optimization.sequence_explanation import SequenceExplanationBuilder


class SequenceDetailedReport:
    def __init__(self, explanation_builder=None):
        self.explanation_builder = explanation_builder or SequenceExplanationBuilder()

    def build(self, sequence_score) -> dict:
        explanation = self.explanation_builder.build(sequence_score)
        return {
            "summary": explanation.summary,
            "strengths": list(explanation.strengths),
            "risks": list(explanation.risks),
            "recommendation": explanation.recommendation,
            "score": sequence_score.score,
            "risk": sequence_score.risk,
            "estimated_delta": sequence_score.sequence.estimated_delta,
            "length": sequence_score.sequence.length,
            "steps": [
                {
                    "order": step.order,
                    "session_id": step.session_id,
                    "day": step.day,
                    "period": step.period,
                    "estimated_delta": step.estimated_delta,
                    "title": step.title,
                }
                for step in sequence_score.sequence.steps
            ],
        }

    def build_text(self, sequence_score) -> str:
        report = self.build(sequence_score)
        lines = [
            "Informe de cadena IA",
            "",
            report["summary"],
            f"Score: {report['score']}",
            f"Riesgo: {report['risk']}",
            f"Mejora estimada: +{report['estimated_delta']}",
            "",
            "Fortalezas:",
        ]
        lines.extend(f"• {item}" for item in report["strengths"])
        lines.append("")
        lines.append("Riesgos:")
        lines.extend(f"• {item}" for item in report["risks"])
        lines.append("")
        lines.append("Pasos:")
        for step in report["steps"]:
            lines.append(
                f"{step['order']}. {step['title']} · sesión {step['session_id']} "
                f"→ día {step['day']}, periodo {step['period']} · +{step['estimated_delta']}"
            )
        lines.append("")
        lines.append("Recomendación:")
        lines.append(report["recommendation"])
        return "\n".join(lines)
