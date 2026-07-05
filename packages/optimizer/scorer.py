from .objective import DEFAULT_WEIGHTS
class Scorer:
    def score(self,solution):
        penalty=len(solution.conflicts)*10
        solution.score=max(0,100-penalty)
        return solution.score
