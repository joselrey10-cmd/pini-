from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class UndoRedoStack:
    _undo: list[object] = field(default_factory=list)
    _redo: list[object] = field(default_factory=list)

    def push(self, action) -> None:
        self._undo.append(action)
        self._redo.clear()

    def can_undo(self) -> bool:
        return bool(self._undo)

    def can_redo(self) -> bool:
        return bool(self._redo)

    def undo(self):
        if not self._undo:
            return None

        action = self._undo.pop()
        self._redo.append(action)
        return action

    def redo(self):
        if not self._redo:
            return None

        action = self._redo.pop()
        self._undo.append(action)
        return action

    def clear(self):
        self._undo.clear()
        self._redo.clear()