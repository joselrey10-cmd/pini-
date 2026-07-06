from packages.substitution.engine import SubstitutionEngine
from packages.substitution.models import Absence, CandidateTeacher


def test_engine_orders_candidates_by_score():
    absence = Absence("Ana", 1, 1, required_speciality="Primaria")
    candidates = [
        CandidateTeacher("Pedro", speciality="Música", is_free=True),
        CandidateTeacher("Luis", speciality="Primaria", is_free=True, is_on_duty=True),
        CandidateTeacher("Ana", speciality="Primaria", is_free=True),
    ]

    proposals = SubstitutionEngine().propose(absence, candidates)

    assert proposals[0].candidate.name == "Luis"
    assert all(p.candidate.name != "Ana" for p in proposals)
