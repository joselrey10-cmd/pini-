from packages.optimizer.solution import Solution
from packages.optimizer.optimizer import Optimizer
def test_optimizer_returns_solution():
    s=Solution()
    result=Optimizer().optimize(s)
    assert result.solution.score==100
