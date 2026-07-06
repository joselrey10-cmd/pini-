from packages.optimizer.models import Session
from packages.optimizer.solution import Solution
from packages.optimizer.premium_optimizer import PremiumOptimizer
from packages.optimizer.premium_report import PremiumOptimizationReport

def test_premium_optimizer():
    s=Solution(sessions=[
        Session("Ana","1A","Lengua","A1",1,1),
        Session("Luis","2A","Mate","A2",1,2)
    ])
    r=PremiumOptimizer(workers=2,candidates_per_worker=5).optimize(s)
    assert r.explored==10
    assert 0<=r.best_score<=100

def test_premium_report():
    s=Solution(sessions=[Session("Ana","1A","Lengua","A1",1,1)])
    rep=PremiumOptimizationReport().build(s,workers=2,candidates_per_worker=3)
    assert rep["explored"]==6
