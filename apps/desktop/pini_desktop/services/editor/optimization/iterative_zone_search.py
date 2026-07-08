from dataclasses import dataclass

from pini_desktop.services.editor.optimization.zone_definition import ZoneDefinition
from pini_desktop.services.editor.optimization.zone_optimizer import ZoneOptimizer, ZoneOptimizationSuggestion


@dataclass(frozen=True)
class IterativeZoneStep:
    iteration: int
    suggestion: ZoneOptimizationSuggestion
    accumulated_delta: float


@dataclass(frozen=True)
class IterativeZoneSearchResult:
    zone: ZoneDefinition
    iterations: int
    steps: tuple[IterativeZoneStep, ...]
    accumulated_delta: float

    @property
    def has_improvement(self) -> bool:
        return self.accumulated_delta > 0


class IterativeZoneSearch:
    """Búsqueda iterativa inicial dentro de una zona.

    No aplica cambios todavía. Encadena las mejores sugerencias estimadas para
    preparar el futuro optimizador automático por zonas.
    """

    def __init__(self, zone_optimizer: ZoneOptimizer | None = None):
        self.zone_optimizer = zone_optimizer or ZoneOptimizer()

    def search(self, zone: ZoneDefinition, max_iterations: int = 3, suggestions_per_iteration: int = 5) -> IterativeZoneSearchResult:
        steps = []
        accumulated = 0.0
        used = set()

        for iteration in range(1, max_iterations + 1):
            result = self.zone_optimizer.optimize(zone, limit=suggestions_per_iteration)
            available = [
                suggestion
                for suggestion in result.suggestions
                if (suggestion.session_id, suggestion.day, suggestion.period) not in used
            ]

            if not available:
                break

            best = available[0]
            if best.estimated_delta <= 0:
                break

            used.add((best.session_id, best.day, best.period))
            accumulated = round(accumulated + best.estimated_delta, 2)

            steps.append(
                IterativeZoneStep(
                    iteration=iteration,
                    suggestion=best,
                    accumulated_delta=accumulated,
                )
            )

        return IterativeZoneSearchResult(
            zone=zone,
            iterations=len(steps),
            steps=tuple(steps),
            accumulated_delta=accumulated,
        )
