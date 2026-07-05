from packages.optimizer.multiobjective import MultiObjectiveScorer, OptimizationWeights

def test_normalization():
    w=OptimizationWeights(30,30,20,20).normalize()
    assert round(w.constraints+w.teacher+w.student+w.rooms,5)==1

def test_combination():
    scorer=MultiObjectiveScorer()
    score=scorer.combine(100,80,90,70)
    assert 0<=score<=100
