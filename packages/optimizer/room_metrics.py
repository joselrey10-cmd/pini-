from dataclasses import dataclass

@dataclass
class RoomMetrics:
    conflicts:int=0
    unsuitable_assignments:int=0
    utilization:int=0
    score:int=100

class RoomMetricsAnalyzer:
    SPECIAL={
        "EF":"Gimnasio",
        "Música":"Aula Música",
        "Informática":"Informática",
    }

    def analyse(self,solution):
        rooms={}
        occ={}
        for s in solution.sessions:
            m=rooms.setdefault(s.room,RoomMetrics())
            occ[(s.room,s.day,s.period)]=occ.get((s.room,s.day,s.period),0)+1
            m.utilization+=1
            expected=self.SPECIAL.get(s.subject)
            if expected and expected!=s.room:
                m.unsuitable_assignments+=1
        for key,count in occ.items():
            if count>1:
                rooms[key[0]].conflicts+=count-1
        for m in rooms.values():
            penalty=m.conflicts*20+m.unsuitable_assignments*10
            m.score=max(0,100-penalty)
        return rooms
