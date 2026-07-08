from dataclasses import dataclass
from typing import Literal

ZoneType = Literal["teacher", "course", "room", "time"]

@dataclass(frozen=True)
class ZoneDefinition:
    zone_type: ZoneType
    entity_id: int | None = None
    day: int | None = None
    start_period: int | None = None
    end_period: int | None = None
    label: str = ""

    def describe(self) -> str:
        if self.zone_type == "time":
            return f"Tramo horario: día {self.day}, periodos {self.start_period}-{self.end_period}"
        return f"{self.zone_type}: {self.label or self.entity_id}"
