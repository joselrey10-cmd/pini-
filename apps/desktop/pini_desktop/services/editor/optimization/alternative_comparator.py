from dataclasses import dataclass

from pini_desktop.services.editor.optimization.alternative_generator import EditorAlternative


@dataclass(frozen=True)
class AlternativeComparisonItem:
    rank: int
    alternative: EditorAlternative
    strengths: tuple[str, ...]
    weaknesses: tuple[str, ...]
    recommendation: str


@dataclass(frozen=True)
class AlternativeComparisonResult:
    items: tuple[AlternativeComparisonItem, ...]
    best: AlternativeComparisonItem | None = None

    @property
    def has_best(self) -> bool:
        return self.best is not None


class AlternativeComparator:
    """Compara alternativas y genera una recomendación clara."""

    def compare(self, alternatives: list[EditorAlternative] | tuple[EditorAlternative, ...]) -> AlternativeComparisonResult:
        ordered = sorted(
            alternatives,
            key=lambda item: (item.estimated_delta, item.estimated_score),
            reverse=True,
        )

        items = []
        for index, alternative in enumerate(ordered, start=1):
            strengths = self._strengths(alternative)
            weaknesses = self._weaknesses(alternative)
            recommendation = self._recommendation(index, alternative, strengths, weaknesses)

            items.append(
                AlternativeComparisonItem(
                    rank=index,
                    alternative=alternative,
                    strengths=strengths,
                    weaknesses=weaknesses,
                    recommendation=recommendation,
                )
            )

        return AlternativeComparisonResult(
            items=tuple(items),
            best=items[0] if items else None,
        )

    def _strengths(self, alternative: EditorAlternative) -> tuple[str, ...]:
        strengths = []

        if alternative.estimated_delta > 1:
            strengths.append("Mejora clara de la puntuación estimada.")
        elif alternative.estimated_delta > 0:
            strengths.append("Mejora moderada de la puntuación estimada.")

        for bullet in alternative.bullets:
            if "última hora" in bullet.lower() and "penalización" not in bullet.lower():
                strengths.append("Puede mejorar la distribución dentro de la jornada.")
            elif "reparto" in bullet.lower():
                strengths.append("Favorece un reparto más equilibrado.")
            elif "riesgo" in bullet.lower():
                strengths.append("Movimiento cercano y de bajo riesgo.")

        if not strengths:
            strengths.append("Mantiene la coherencia básica del horario.")

        return tuple(dict.fromkeys(strengths))

    def _weaknesses(self, alternative: EditorAlternative) -> tuple[str, ...]:
        weaknesses = []

        for bullet in alternative.bullets:
            text = bullet.lower()
            if "penalización" in text:
                weaknesses.append("Puede situar la sesión en una franja menos favorable.")
            if "requiere revisión" in text:
                weaknesses.append("Conviene revisar el impacto antes de aplicarla.")

        if alternative.estimated_delta <= 0:
            weaknesses.append("No aporta mejora estimada.")

        return tuple(dict.fromkeys(weaknesses))

    def _recommendation(self, rank: int, alternative: EditorAlternative, strengths, weaknesses) -> str:
        if rank == 1 and alternative.estimated_delta > 0:
            return "Recomendada como mejor alternativa."
        if alternative.estimated_delta > 0 and not weaknesses:
            return "Alternativa positiva."
        if weaknesses:
            return "Aplicar solo tras revisión."
        return "Alternativa neutra."
