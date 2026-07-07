from pini_desktop.services.editor.history import UndoStack


class DummyCommand:
    name = "dummy"

    def __init__(self):
        self.executed = 0
        self.undone = 0

    def execute(self):
        self.executed += 1

    def undo(self):
        self.undone += 1

    def redo(self):
        self.execute()


def test_undo_stack_push_undo_redo_clear():
    stack = UndoStack()
    command = DummyCommand()
    stack.push(command)

    assert stack.can_undo
    assert stack.size == 1

    assert stack.undo() is command
    assert command.undone == 1
    assert stack.can_redo

    assert stack.redo() is command
    assert command.executed == 1
    assert stack.can_undo

    stack.clear()
    assert not stack.can_undo
    assert not stack.can_redo
