from dataclasses import dataclass


@dataclass(frozen=True)
class AlternativeExplanation:
    summary: str
    bullets: tuple[str, ...]


class ExplanationBuilder:
    """Construye explicaciones legibles para las alternativas del editor."""

    def build(self, estimated_score) -> AlternativeExplanation:
        bullets = []

        for reason in getattr(estimated_score, "reasons", ()) or ():
            bullets.append(self._normalize_reason(reason))

        delta = getattr(estimated_score, "delta", 0.0)

        if delta > 1:
            summary = "Alternativa recomendable: mejora claramente la calidad estimada del horario."
        elif delta > 0:
            summary = "Alternativa válida: aporta una mejora moderada."
        elif delta == 0:
            summary = "Alternativa neutra: no empeora el horario."
        else:
            summary = "Alternativa delicada: puede empeorar el horario y conviene revisarla."

        if not bullets:
            bullets = ["✔ Mantiene la coherencia básica del horario."]

        return AlternativeExplanation(summary=summary, bullets=tuple(bullets))

    def _normalize_reason(self, reason: str) -> str:
        text = str(reason).strip()
        if not text:
            return "✔ Mejora general del horario."
        if text.startswith("✔"):
            return text
        if text.startswith("✓") or text.startswith("√") or text.startswith("•"):
            text = text[1:].strip()
        return f"✔ {text}"