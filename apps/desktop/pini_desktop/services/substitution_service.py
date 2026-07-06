from dataclasses import dataclass

from pini_desktop.config.settings import DATABASE_PATH
from packages.substitution.service import SubstitutionService as CoreSubstitutionService


@dataclass(frozen=True)
class PiniSubstitutionProposal:
    teacher: str
    score: int
    reasons: tuple[str, ...]
    warnings: tuple[str, ...]


class PiniSubstitutionService:
    def __init__(self, database_path=DATABASE_PATH):
        self.core = CoreSubstitutionService(database_path=database_path)

    def propose_for_absence(self, absent_teacher_id: int, day: int, period: int) -> list[PiniSubstitutionProposal]:
        proposals = self.core.propose_from_pini(absent_teacher_id, day, period)
        return [
            PiniSubstitutionProposal(
                teacher=proposal.candidate.name,
                score=proposal.score,
                reasons=tuple(proposal.reasons),
                warnings=tuple(proposal.warnings),
            )
            for proposal in proposals
        ]
