from dataclasses import dataclass, field
@dataclass
class Session:
    teacher:str
    course:str
    subject:str
    room:str
    day:int
    period:int
