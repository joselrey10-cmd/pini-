from .availability import SubstitutionAvailability
from .models import Absence, CandidateTeacher, SubstitutionProposal
from .ranking import SubstitutionRanker


class SubstitutionEngine:
    def __init__(self):
        self.availability = SubstitutionAvailability()
        self.ranker = SubstitutionRanker()

    def propose(
        self,
        absence: Absence,
        candidates: list[CandidateTeacher],
        limit: int = 5,
    ) -> list[SubstitutionProposal]:
        proposals = []

        for candidate in candidates:
            if not self.availability.is_available(absence, candidate):
                continue
            proposals.append(self.ranker.rank(absence, candidate))

        proposals.sort(key=lambda item: item.score, reverse=True)
        return proposals[:limit]
