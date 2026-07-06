from dataclasses import dataclass, field

from .engine import SubstitutionEngine
from .models import Absence, CandidateTeacher, SubstitutionProposal


@dataclass
class PeriodSubstitutionPlan:
    absence: Absence
    proposals: list[SubstitutionProposal] = field(default_factory=list)


@dataclass
class MultiPeriodSubstitutionPlan:
    teacher: str
    day: int
    periods: list[int]
    plans: list[PeriodSubstitutionPlan] = field(default_factory=list)

    @property
    def fully_covered(self) -> bool:
        return all(plan.proposals for plan in self.plans)

    @property
    def uncovered_periods(self) -> list[int]:
        return [plan.absence.period for plan in self.plans if not plan.proposals]


class MultiPeriodSubstitutionEngine:
    def __init__(self):
        self.engine = SubstitutionEngine()

    def propose(
        self,
        absences: list[Absence],
        candidates_by_period: dict[int, list[CandidateTeacher]],
        limit: int = 5,
    ) -> MultiPeriodSubstitutionPlan:
        if not absences:
            return MultiPeriodSubstitutionPlan(teacher="", day=0, periods=[], plans=[])

        teacher = absences[0].teacher
        day = absences[0].day
        plans = []

        for absence in absences:
            candidates = candidates_by_period.get(absence.period, [])
            proposals = self.engine.propose(absence, candidates, limit=limit)
            plans.append(PeriodSubstitutionPlan(absence=absence, proposals=proposals))

        return MultiPeriodSubstitutionPlan(
            teacher=teacher,
            day=day,
            periods=[absence.period for absence in absences],
            plans=plans,
        )
