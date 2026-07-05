from .constraints import ConstraintEngine
from .scorer import Scorer
from .neighbourhood import Neighbourhood
class Optimizer:
    def __init__(self):
        self.constraints=ConstraintEngine()
        self.scorer=Scorer()
        self.neighbourhood=Neighbourhood()
    def optimize(self,solution):
        solution.conflicts=self.constraints.evaluate(solution)
        self.scorer.score(solution)
        return solution
