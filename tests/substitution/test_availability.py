from packages.substitution.availability import SubstitutionAvailability
from packages.substitution.models import Absence, CandidateTeacher


def test_absent_teacher_is_not_available():
    absence = Absence("Ana", 1, 1)
    candidate = CandidateTeacher("Ana", is_free=True)

    assert not SubstitutionAvailability().is_available(absence, candidate)


def test_free_teacher_is_available():
    absence = Absence("Ana", 1, 1)
    candidate = CandidateTeacher("Luis", is_free=True)

    assert SubstitutionAvailability().is_available(absence, candidate)
