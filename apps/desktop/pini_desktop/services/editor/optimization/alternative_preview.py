from dataclasses import dataclass

from pini_desktop.services.editor.optimization.alternative_generator import EditorAlternative


@dataclass(frozen=True)
class AlternativePreview:
    title: str
    destination: str
    estimated_delta: float
    estimated_score: float
    explanation: str
    bullets: tuple[str, ...]
    can_apply: bool = True


class AlternativePreviewService:
    def build_preview(self, alternative: EditorAlternative) -> AlternativePreview:
        candidate = alternative.candidate
        return AlternativePreview(
            title=alternative.title,
            destination=f"Día {candidate.day}, periodo {candidate.period}",
            estimated_delta=alternative.estimated_delta,
            estimated_score=alternative.estimated_score,
            explanation=alternative.explanation,
            bullets=alternative.bullets,
            can_apply=True,
        )

    def build_text(self, alternative: EditorAlternative) -> str:
        preview = self.build_preview(alternative)
        lines = [
            preview.title,
            f"Destino: {preview.destination}",
            f"Mejora estimada: +{preview.estimated_delta}",
            f"Score estimado: {preview.estimated_score}",
            "",
            preview.explanation,
            "",
            "Motivos:",
        ]
        lines.extend(f"• {bullet.replace('✔ ', '')}" for bullet in preview.bullets)
        return "\n".join(lines)
