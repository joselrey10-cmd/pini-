from dataclasses import dataclass

@dataclass(frozen=True)
class RuleParameter:
    rule_code: str
    key: str
    value: str
