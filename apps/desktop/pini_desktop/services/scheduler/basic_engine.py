from pini_desktop.services.rule_runtime_service import RuleRuntimeService
from pini_desktop.services.scheduler.domain import (
    ScheduleGenerationResult,
    SchedulePlacement,
)
from pini_desktop.services.scheduler.repository import SchedulerRepository


class BasicSchedulerEngine:
    """Generador básico intercambiable.

    Este motor no optimiza todavía. Su objetivo es colocar sesiones respetando
    conflictos básicos y reglas dinámicas simples.
    """

    GENERATED_BY = "basic-engine-v1"

    def __init__(self, repository: SchedulerRepository, rule_runtime: RuleRuntimeService):
        self.repository = repository
        self.rule_runtime = rule_runtime

    def generate(self) -> ScheduleGenerationResult:
        periods = self.repository.list_periods()
        assignments = self.repository.list_assignments()

        if not periods:
            return ScheduleGenerationResult([], ["No hay periodos generados."])

        placements: list[SchedulePlacement] = []
        warnings: list[str] = []

        occupied_course: set[tuple[int, int, int]] = set()
        occupied_teacher: set[tuple[int, int, int]] = set()
        occupied_room: set[tuple[int, int, int]] = set()

        for assignment in assignments:
            placed = 0

            candidate_periods = sorted(
                periods,
                key=lambda period: self.rule_runtime.preferred_period_score(
                    course_code=assignment.course_code,
                    subject_name=assignment.subject_name,
                    teacher_name=self.repository.teacher_name(assignment.preferred_teacher_id),
                    room_type=assignment.required_room_type,
                    day=period.day,
                    period=period.period,
                ),
                reverse=True,
            )

            for period in candidate_periods:
                if placed >= assignment.weekly_sessions:
                    break

                teacher_id = assignment.preferred_teacher_id
                teacher_name = self.repository.teacher_name(teacher_id)
                room_id = self.repository.find_room(assignment.required_room_type)

                decision = self.rule_runtime.is_period_allowed(
                    course_code=assignment.course_code,
                    subject_name=assignment.subject_name,
                    teacher_name=teacher_name,
                    room_type=assignment.required_room_type,
                    day=period.day,
                    period=period.period,
                    is_after_break=period.is_after_break,
                )
                if not decision.allowed:
                    continue

                if (assignment.course_id, period.day, period.period) in occupied_course:
                    continue
                if teacher_id is not None and (int(teacher_id), period.day, period.period) in occupied_teacher:
                    continue
                if room_id is not None and (int(room_id), period.day, period.period) in occupied_room:
                    continue
                if teacher_id is not None and self.repository.teacher_forbidden(int(teacher_id), period.day, period.period):
                    continue

                placements.append(
                    SchedulePlacement(
                        course_id=assignment.course_id,
                        subject_id=assignment.subject_id,
                        teacher_id=int(teacher_id) if teacher_id is not None else None,
                        room_id=int(room_id) if room_id is not None else None,
                        day=period.day,
                        period=period.period,
                        generated_by=self.GENERATED_BY,
                    )
                )

                occupied_course.add((assignment.course_id, period.day, period.period))
                if teacher_id is not None:
                    occupied_teacher.add((int(teacher_id), period.day, period.period))
                if room_id is not None:
                    occupied_room.add((int(room_id), period.day, period.period))

                placed += 1

            if placed < assignment.weekly_sessions:
                warnings.append(
                    f"No se pudieron colocar todas las sesiones de {assignment.subject_name} en {assignment.course_code} ({placed}/{assignment.weekly_sessions})."
                )

        return ScheduleGenerationResult(placements, warnings)
