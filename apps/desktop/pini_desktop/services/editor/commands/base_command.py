from abc import ABC, abstractmethod


class EditorCommand(ABC):
    name = "editor_command"

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    @abstractmethod
    def undo(self):
        raise NotImplementedError

    def redo(self):
        return self.execute()
