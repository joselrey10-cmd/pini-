from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class HistoryEntry:
    timestamp: datetime
    description: str
    score_delta: float


@dataclass(slots=True)
class HistoryService:
    _entries: list[HistoryEntry] = field(default_factory=list)

    def add(self, description: str, score_delta: float) -> None:
        self._entries.append(
            HistoryEntry(
                timestamp=datetime.now(),
                description=description,
                score_delta=score_delta,
            )
        )

    def entries(self) -> tuple[HistoryEntry, ...]:
        return tuple(self._entries)

    def clear(self) -> None:
        self._entries.clear()