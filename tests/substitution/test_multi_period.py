from packages.substitution.models import Absence, CandidateTeacher
from packages.substitution.multi_period import MultiPeriodSubstitutionEngine


def test_multi_period_plan_detects_full_coverage():
    absences = [
        Absence("Ana", 1, 1, required_speciality="Primaria"),
        Absence("Ana", 1, 2, required_speciality="Primaria"),
    ]
    candidates_by_period = {
        1: [CandidateTeacher("Luis", speciality="Primaria", is_free=True)],
        2: [CandidateTeacher("Marta", speciality="Primaria", is_free=True)],
    }

    plan = MultiPeriodSubstitutionEngine().propose(absences, candidates_by_period)

    assert plan.fully_covered
    assert plan.uncovered_periods == []
    assert len(plan.plans) == 2


def test_multi_period_plan_detects_uncovered_period():
    absences = [
        Absence("Ana", 1, 1),
        Absence("Ana", 1, 2),
    ]
    candidates_by_period = {
        1: [CandidateTeacher("Luis", is_free=True)],
        2: [],
    }

    plan = MultiPeriodSubstitutionEngine().propose(absences, candidates_by_period)

    assert not plan.fully_covered
    assert plan.uncovered_periods == [2]
