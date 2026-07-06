from dataclasses import dataclass

from pini_desktop.config.settings import DATABASE_PATH
from packages.substitution.service import SubstitutionService as CoreSubstitutionService


@dataclass(frozen=True)
class PiniSubstitutionProposal:
    teacher: str
    score: int
    reasons: tuple[str, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class PiniPeriodSubstitutionPlan:
    period: int
    proposals: tuple[PiniSubstitutionProposal, ...]


class PiniSubstitutionService:
    def __init__(self, database_path=DATABASE_PATH):
        self.core = CoreSubstitutionService(database_path=database_path)

    def propose_for_absence(self, absent_teacher_id: int, day: int, period: int) -> list[PiniSubstitutionProposal]:
        proposals = self.core.propose_from_pini(absent_teacher_id, day, period)
        return [self._proposal(item) for item in proposals]

    def propose_for_absence_range(self, absent_teacher_id: int, day: int, start_period: int, end_period: int) -> list[PiniPeriodSubstitutionPlan]:
        plan = self.core.propose_range_from_pini(absent_teacher_id, day, start_period, end_period)
        return [
            PiniPeriodSubstitutionPlan(
                period=item.absence.period,
                proposals=tuple(self._proposal(proposal) for proposal in item.proposals),
            )
            for item in plan.plans
        ]

    def _proposal(self, proposal) -> PiniSubstitutionProposal:
        return PiniSubstitutionProposal(
            teacher=proposal.candidate.name,
            score=proposal.score,
            reasons=tuple(proposal.reasons),
            warnings=tuple(proposal.warnings),
        )
