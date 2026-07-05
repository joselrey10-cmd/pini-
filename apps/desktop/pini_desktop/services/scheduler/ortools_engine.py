from pini_desktop.services.scheduler.domain import ScheduleGenerationResult


class OrToolsSchedulerEngine:
    """Placeholder del futuro solver OR-Tools.

    Esta clase permite dejar preparada la arquitectura sin activar todavía
    la dependencia ni el modelo CP-SAT completo.
    """

    def generate(self) -> ScheduleGenerationResult:
        return ScheduleGenerationResult(
            placements=[],
            warnings=["El motor OR-Tools todavía no está implementado. Usa el generador básico."],
        )
