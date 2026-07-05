from .scorer import Scorer

class QualityReport:
    def build(self, solution):
        s=Scorer().evaluate(solution)
        return {
            "score": s.total,
            "teacher_gaps": s.teacher_gaps,
            "distribution": s.distribution,
            "room_usage": s.room_usage,
            "constraints": s.constraints,
            "conflicts": list(getattr(solution,"conflicts",[])),
        }
