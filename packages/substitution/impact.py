from .models import CandidateTeacher


class ImpactAnalyzer:
    def impact_penalty(self, candidate: CandidateTeacher) -> int:
        penalty = 0

        if candidate.breaks_important_support:
            penalty += 35
        elif candidate.can_move_support:
            penalty += 10

        if candidate.current_task:
            penalty += 5

        if not candidate.same_building:
            penalty += 5

        return penalty
