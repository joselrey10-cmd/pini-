from dataclasses import dataclass

from pini_desktop.services.editor.editor_service import EditorService


@dataclass(frozen=True)
class LocalOptimizationSuggestion:
    title: str
    description: str
    estimated_delta: float
    action_type: str
    payload: dict


@dataclass(frozen=True)
class LocalOptimizationResult:
    suggestions: tuple[LocalOptimizationSuggestion, ...]
    best_delta: float = 0.0

    @property
    def has_suggestions(self) -> bool:
        return bool(self.suggestions)


class LocalOptimizationService:
    """Optimizador local inicial.

    Esta primera versión no modifica automáticamente el horario. Analiza la zona
    afectada y devuelve sugerencias seguras para el usuario.
    """

    def __init__(self, editor_service: EditorService | None = None):
        self.editor_service = editor_service or EditorService()

    def analyse_after_move(self, result) -> LocalOptimizationResult:
        if not getattr(result, "success", False):
            return LocalOptimizationResult(suggestions=())

        old_score = getattr(result, "old_score", None)
        new_score = getattr(result, "new_score", None)
        suggestions = []

        if old_score is not None and new_score is not None:
            delta = round(float(new_score) - float(old_score), 2)
            if delta < 0:
                suggestions.append(
                    LocalOptimizationSuggestion(
                        title="Revisar zona afectada",
                        description="El cambio reduce la puntuación. Conviene revisar profesor, grupo y aula afectados.",
                        estimated_delta=abs(delta),
                        action_type="review",
                        payload={"reason": "score_drop", "delta": delta},
                    )
                )
            elif delta == 0:
                suggestions.append(
                    LocalOptimizationSuggestion(
                        title="Buscar mejora local",
                        description="El cambio mantiene la puntuación. Pini puede intentar buscar una mejora pequeña en la zona afectada.",
                        estimated_delta=0.5,
                        action_type="local_search",
                        payload={"reason": "neutral_move"},
                    )
                )
            else:
                suggestions.append(
                    LocalOptimizationSuggestion(
                        title="Conservar cambio",
                        description="El cambio mejora el horario. Se recomienda mantenerlo.",
                        estimated_delta=delta,
                        action_type="keep",
                        payload={"reason": "score_improved", "delta": delta},
                    )
                )
        else:
            suggestions.append(
                LocalOptimizationSuggestion(
                    title="Analizar impacto",
                    description="No hay puntuación suficiente para estimar mejora. Se recomienda revisar el panel de impacto.",
                    estimated_delta=0.0,
                    action_type="inspect",
                    payload={"reason": "missing_score"},
                )
            )

        best_delta = max((item.estimated_delta for item in suggestions), default=0.0)
        return LocalOptimizationResult(suggestions=tuple(suggestions), best_delta=best_delta)
