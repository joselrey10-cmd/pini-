from packages.substitution.models import Absence, CandidateTeacher
from packages.substitution.ranking import SubstitutionRanker


def test_on_duty_specialist_scores_high():
    absence = Absence("Ana", 1, 1, required_speciality="Primaria")
    candidate = CandidateTeacher("Luis", speciality="Primaria", is_free=True, is_on_duty=True)

    proposal = SubstitutionRanker().rank(absence, candidate)

    assert proposal.score >= 90
    assert "Está de guardia" in proposal.reasons


def test_important_support_penalizes_candidate():
    absence = Absence("Ana", 1, 1, required_speciality="Primaria")
    candidate = CandidateTeacher(
        "Marta",
        speciality="Primaria",
        is_free=False,
        can_move_support=True,
        breaks_important_support=True,
    )

    proposal = SubstitutionRanker().rank(absence, candidate)

    assert proposal.score < 70
    assert proposal.warnings
