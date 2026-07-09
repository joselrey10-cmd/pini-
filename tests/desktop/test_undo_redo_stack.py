from pini_desktop.services.editor.optimization.undo_redo_stack import (
    UndoRedoStack,
)


def test_push_enables_undo():
    stack = UndoRedoStack()

    stack.push("A")

    assert stack.can_undo()
    assert not stack.can_redo()


def test_undo_moves_action_to_redo():
    stack = UndoRedoStack()

    stack.push("A")

    action = stack.undo()

    assert action == "A"
    assert not stack.can_undo()
    assert stack.can_redo()


def test_redo_restores_action():
    stack = UndoRedoStack()

    stack.push("A")
    stack.undo()

    action = stack.redo()

    assert action == "A"
    assert stack.can_undo()


def test_clear_empties_everything():
    stack = UndoRedoStack()

    stack.push("A")
    stack.clear()

    assert not stack.can_undo()
    assert not stack.can_redo()