from .engine import SubstitutionEngine
from .models import Absence, CandidateTeacher


class SubstitutionService:
    """Fachada inicial del módulo de sustituciones.

    En próximos sprints se conectará con la base de datos real de Pini.
    """

    def __init__(self):
        self.engine = SubstitutionEngine()

    def propose_substitutions(self, absence: Absence, candidates: list[CandidateTeacher]):
        return self.engine.propose(absence, candidates)
