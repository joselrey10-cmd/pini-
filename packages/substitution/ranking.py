from .impact import ImpactAnalyzer
from .models import Absence, CandidateTeacher, SubstitutionProposal


class SubstitutionRanker:
    def __init__(self):
        self.impact = ImpactAnalyzer()

    def rank(self, absence: Absence, candidate: CandidateTeacher) -> SubstitutionProposal:
        score = 50
        reasons = []
        warnings = []

        if candidate.is_free:
            score += 25
            reasons.append("Libre en esa franja")

        if candidate.is_on_duty:
            score += 20
            reasons.append("Está de guardia")

        if absence.required_speciality and candidate.speciality == absence.required_speciality:
            score += 20
            reasons.append("Especialidad compatible")
        elif absence.required_speciality and candidate.speciality != absence.required_speciality:
            score -= 10
            warnings.append("Especialidad no coincidente")

        if candidate.same_building:
            score += 5
            reasons.append("Mismo edificio")
        else:
            warnings.append("Requiere desplazamiento")

        if candidate.can_move_support:
            reasons.append("Puede mover apoyo")

        if candidate.breaks_important_support:
            warnings.append("Rompe un apoyo importante")

        score -= self.impact.impact_penalty(candidate)
        score = max(0, min(100, score))

        return SubstitutionProposal(
            candidate=candidate,
            score=score,
            reasons=reasons,
            warnings=warnings,
        )
