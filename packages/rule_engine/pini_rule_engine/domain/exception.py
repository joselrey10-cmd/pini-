from dataclasses import dataclass

@dataclass(frozen=True)
class RuleException:
    rule_code: str
    subject: str
    course_from: int
    course_to: int
    parameter: str
    value: str

    def applies_to(self, subject: str, course_level: int) -> bool:
        return self.subject.casefold() == subject.casefold() and self.course_from <= course_level <= self.course_to
