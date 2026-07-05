from dataclasses import dataclass
from .multiobjective import OptimizationWeights

@dataclass
class OptimizationProfile:
    name:str
    weights:OptimizationWeights

BALANCED=OptimizationProfile(
    "Balanced",
    OptimizationWeights()
)

TEACHER_FIRST=OptimizationProfile(
    "Teacher First",
    OptimizationWeights(0.25,0.45,0.15,0.15)
)

STUDENT_FIRST=OptimizationProfile(
    "Student First",
    OptimizationWeights(0.25,0.15,0.45,0.15)
)

ROOM_FIRST=OptimizationProfile(
    "Rooms First",
    OptimizationWeights(0.20,0.20,0.20,0.40)
)
