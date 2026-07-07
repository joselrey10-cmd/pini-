from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HistoryEntry:
    command_name: str
    description: str
    created_at: str

    @classmethod
    def from_command(cls, command, description: str = ""):
        return cls(
            command_name=getattr(command, "name", command.__class__.__name__),
            description=description or getattr(command, "name", command.__class__.__name__),
            created_at=datetime.now().isoformat(timespec="seconds"),
        )
