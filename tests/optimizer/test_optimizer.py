from packages.optimizer.solution import Solution
from packages.optimizer.optimizer import Optimizer
def test_optimizer_returns_solution():
    s=Solution()
    r=Optimizer().optimize(s)
    assert r.score==100
