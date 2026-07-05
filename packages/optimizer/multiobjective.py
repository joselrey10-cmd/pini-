from dataclasses import dataclass

@dataclass
class OptimizationWeights:
    constraints: float = 0.30
    teacher: float = 0.25
    student: float = 0.25
    rooms: float = 0.20

    def normalize(self):
        total=self.constraints+self.teacher+self.student+self.rooms
        if total<=0:
            raise ValueError("Weight sum must be positive")
        self.constraints/=total
        self.teacher/=total
        self.student/=total
        self.rooms/=total
        return self

class MultiObjectiveScorer:
    def __init__(self,weights=None):
        self.weights=(weights or OptimizationWeights()).normalize()

    def combine(self,constraints,teacher,student,rooms):
        w=self.weights
        return round(
            constraints*w.constraints+
            teacher*w.teacher+
            student*w.student+
            rooms*w.rooms,2)
