from packages.optimizer.solution import Solution
from packages.optimizer.scorer import Scorer

def test_score_without_conflicts():
    score=Scorer().evaluate(Solution())
    assert score.total==100

def test_score_with_conflicts():
    s=Solution()
    s.conflicts=["A","B"]
    score=Scorer().evaluate(s)
    assert score.total<100
