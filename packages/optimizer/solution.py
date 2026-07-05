from dataclasses import dataclass, field
from .models import Session
@dataclass
class Solution:
    sessions:list[Session]=field(default_factory=list)
    score:float=0.0
    conflicts:list[str]=field(default_factory=list)
