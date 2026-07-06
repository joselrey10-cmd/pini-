from .engine import SubstitutionEngine
from .models import Absence, CandidateTeacher
from .pini_adapter import PiniSubstitutionDataAdapter


class SubstitutionService:
    """Fachada del módulo de sustituciones.

    Puede trabajar con candidatos manuales o con datos reales de Pini si se
    proporciona una base de datos.
    """

    def __init__(self, database_path=None):
        self.engine = SubstitutionEngine()
        self.adapter = PiniSubstitutionDataAdapter(database_path) if database_path else None

    def propose_substitutions(self, absence: Absence, candidates: list[CandidateTeacher]):
        return self.engine.propose(absence, candidates)

    def propose_from_pini(self, absent_teacher_id: int, day: int, period: int, limit: int = 5):
        if self.adapter is None:
            raise ValueError("No se ha configurado database_path para leer datos de Pini.")

        absence = self.adapter.absence_from_teacher_period(absent_teacher_id, day, period)
        candidates = self.adapter.candidate_teachers(absent_teacher_id, day, period)
        return self.engine.propose(absence, candidates, limit=limit)
