from .engine import SubstitutionEngine
from .models import Absence, CandidateTeacher
from .multi_period import MultiPeriodSubstitutionEngine
from .pini_adapter import PiniSubstitutionDataAdapter


class SubstitutionService:
    def __init__(self, database_path=None):
        self.engine = SubstitutionEngine()
        self.multi_engine = MultiPeriodSubstitutionEngine()
        self.adapter = PiniSubstitutionDataAdapter(database_path) if database_path else None

    def propose_substitutions(self, absence: Absence, candidates: list[CandidateTeacher]):
        return self.engine.propose(absence, candidates)

    def propose_multi_period(self, absences: list[Absence], candidates_by_period: dict[int, list[CandidateTeacher]]):
        return self.multi_engine.propose(absences, candidates_by_period)

    def propose_from_pini(self, absent_teacher_id: int, day: int, period: int, limit: int = 5):
        if self.adapter is None:
            raise ValueError("No se ha configurado database_path para leer datos de Pini.")
        absence = self.adapter.absence_from_teacher_period(absent_teacher_id, day, period)
        candidates = self.adapter.candidate_teachers(absent_teacher_id, day, period)
        return self.engine.propose(absence, candidates, limit=limit)

    def propose_range_from_pini(self, absent_teacher_id: int, day: int, start_period: int, end_period: int, limit: int = 5):
        if self.adapter is None:
            raise ValueError("No se ha configurado database_path para leer datos de Pini.")
        periods = list(range(start_period, end_period + 1))
        absences = self.adapter.absences_from_teacher_periods(absent_teacher_id, day, periods)
        candidates_by_period = self.adapter.candidates_by_period(absent_teacher_id, day, periods)
        return self.multi_engine.propose(absences, candidates_by_period, limit=limit)
