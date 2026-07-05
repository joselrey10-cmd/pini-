from packages.optimizer.models import Session
from packages.optimizer.solution import Solution
from packages.optimizer.room_metrics import RoomMetricsAnalyzer

def test_room_conflicts():
    s=Solution(sessions=[
        Session("A","1A","EF","Gimnasio",1,1),
        Session("B","2A","Mate","Gimnasio",1,1),
    ])
    r=RoomMetricsAnalyzer().analyse(s)
    assert r["Gimnasio"].conflicts==1

def test_unsuitable_room():
    s=Solution(sessions=[
        Session("A","1A","Informática","Aula 1",1,2),
    ])
    r=RoomMetricsAnalyzer().analyse(s)
    assert r["Aula 1"].unsuitable_assignments==1
