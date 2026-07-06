from .models import Absence, CandidateTeacher


class SubstitutionAvailability:
    def is_available(self, absence: Absence, candidate: CandidateTeacher) -> bool:
        if candidate.name == absence.teacher:
            return False
        if candidate.is_free:
            return True
        if candidate.is_on_duty:
            return True
        if candidate.can_move_support and not candidate.breaks_important_support:
            return True
        return False
