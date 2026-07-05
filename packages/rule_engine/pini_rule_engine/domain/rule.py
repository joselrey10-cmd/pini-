from dataclasses import dataclass
from enum import Enum

class RuleType(str, Enum):
    HARD = "hard"
    SOFT = "soft"
    OPTIMIZATION = "optimization"

@dataclass(frozen=True)
class Rule:
    code: str
    name: str
    category: str
    rule_type: RuleType
    enabled: bool = True
    weight: int = 1000
    description: str = ""
