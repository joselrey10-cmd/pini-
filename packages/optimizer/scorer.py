from dataclasses import dataclass

@dataclass
class ScoreBreakdown:
    teacher_gaps:int=0
    distribution:int=0
    room_usage:int=0
    constraints:int=0
    total:int=0

class Scorer:
    def evaluate(self, solution):
        gaps=max(0,100-len(getattr(solution,"conflicts",[]))*5)
        distribution=100
        room_usage=100
        constraints=max(0,100-len(getattr(solution,"conflicts",[]))*10)
        total=round((gaps+distribution+room_usage+constraints)/4,2)
        return ScoreBreakdown(
            teacher_gaps=gaps,
            distribution=distribution,
            room_usage=room_usage,
            constraints=constraints,
            total=total
        )
