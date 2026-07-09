from __future__ import annotations


class CourseOptimizationSummaryBuilder:
    def build(self, result) -> str:
        if result.analyzed_sessions == 0:
            return "No se han encontrado sesiones para este curso."

        if result.best_delta > 0:
            return (
                f"Se han analizado {result.analyzed_sessions} sesiones. "
                f"La mejor mejora estimada es de {result.best_delta:+.1f} puntos."
            )

        return (
            f"Se han analizado {result.analyzed_sessions} sesiones, "
            "pero no se han encontrado mejoras claras."
        )