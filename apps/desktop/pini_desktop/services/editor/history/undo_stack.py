class UndoStack:
    def __init__(self):
        self._undo = []
        self._redo = []

    @property
    def can_undo(self) -> bool:
        return bool(self._undo)

    @property
    def can_redo(self) -> bool:
        return bool(self._redo)

    @property
    def size(self) -> int:
        return len(self._undo)

    def push(self, command) -> None:
        self._undo.append(command)
        self._redo.clear()

    def undo(self):
        if not self._undo:
            return None
        command = self._undo.pop()
        command.undo()
        self._redo.append(command)
        return command

    def redo(self):
        if not self._redo:
            return None
        command = self._redo.pop()
        command.redo()
        self._undo.append(command)
        return command

    def clear(self) -> None:
        self._undo.clear()
        self._redo.clear()
