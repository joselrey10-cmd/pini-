from ortools.sat.python import cp_model

from pini_desktop.services.scheduler.domain import ScheduleGenerationResult, SchedulePlacement


class OrToolsSchedulerEngine:
    GENERATED_BY = "ortools-cpsat-v1"

    def __init__(self, repository, rule_runtime, max_time_seconds: float = 10.0):
        self.repository = repository
        self.rule_runtime = rule_runtime
        self.max_time_seconds = max_time_seconds

    def generate(self) -> ScheduleGenerationResult:
        periods = self.repository.list_periods()
        assignments = self.repository.list_assignments()

        if not periods:
            return ScheduleGenerationResult([], ["No hay periodos generados."])
        if not assignments:
            return ScheduleGenerationResult([], ["No hay materias asignadas a cursos."])

        model = cp_model.CpModel()
        variables = {}

        for a_idx, assignment in enumerate(assignments):
            teacher_name = self.repository.teacher_name(assignment.preferred_teacher_id)
            for p_idx, period in enumerate(periods):
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

                if assignment.preferred_teacher_id is not None and self.repository.teacher_forbidden(
                    int(assignment.preferred_teacher_id), period.day, period.period
                ):
                    continue

                variables[(a_idx, p_idx)] = model.NewBoolVar(f"a{a_idx}_p{p_idx}")

        warnings = []

        for a_idx, assignment in enumerate(assignments):
            vars_for_assignment = [var for (idx, _), var in variables.items() if idx == a_idx]
            if len(vars_for_assignment) < assignment.weekly_sessions:
                warnings.append(f"No hay huecos suficientes para {assignment.subject_name} en {assignment.course_code}.")
                continue
            model.Add(sum(vars_for_assignment) == assignment.weekly_sessions)

        for p_idx, _period in enumerate(periods):
            for course_id in {a.course_id for a in assignments}:
                vars_for_course = [
                    var for (a_idx, pp_idx), var in variables.items()
                    if pp_idx == p_idx and assignments[a_idx].course_id == course_id
                ]
                if len(vars_for_course) > 1:
                    model.Add(sum(vars_for_course) <= 1)

            teacher_ids = {
                int(a.preferred_teacher_id) for a in assignments
                if a.preferred_teacher_id is not None
            }
            for teacher_id in teacher_ids:
                vars_for_teacher = [
                    var for (a_idx, pp_idx), var in variables.items()
                    if pp_idx == p_idx
                    and assignments[a_idx].preferred_teacher_id is not None
                    and int(assignments[a_idx].preferred_teacher_id) == teacher_id
                ]
                if len(vars_for_teacher) > 1:
                    model.Add(sum(vars_for_teacher) <= 1)

        score_terms = []
        for (a_idx, p_idx), var in variables.items():
            assignment = assignments[a_idx]
            period = periods[p_idx]
            score = self.rule_runtime.preferred_period_score(
                course_code=assignment.course_code,
                subject_name=assignment.subject_name,
                teacher_name=self.repository.teacher_name(assignment.preferred_teacher_id),
                room_type=assignment.required_room_type,
                day=period.day,
                period=period.period,
            )
            if score:
                score_terms.append(score * var)

        if score_terms:
            model.Maximize(sum(score_terms))

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = self.max_time_seconds
        status = solver.Solve(model)

        if status not in {cp_model.OPTIMAL, cp_model.FEASIBLE}:
            return ScheduleGenerationResult([], ["OR-Tools no ha encontrado solución viable."])

        placements = []
        for (a_idx, p_idx), var in variables.items():
            if solver.BooleanValue(var):
                assignment = assignments[a_idx]
                period = periods[p_idx]
                room_id = self.repository.find_room(assignment.required_room_type)
                placements.append(
                    SchedulePlacement(
                        course_id=assignment.course_id,
                        subject_id=assignment.subject_id,
                        teacher_id=int(assignment.preferred_teacher_id) if assignment.preferred_teacher_id is not None else None,
                        room_id=int(room_id) if room_id is not None else None,
                        day=period.day,
                        period=period.period,
                        generated_by=self.GENERATED_BY,
                    )
                )

        return ScheduleGenerationResult(placements, warnings)
