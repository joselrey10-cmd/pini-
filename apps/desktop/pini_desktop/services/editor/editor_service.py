from pathlib import Path

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database
from pini_desktop.services.editor.commands import MoveSessionCommand, SwapSessionsCommand
from pini_desktop.services.editor.history import UndoStack
from pini_desktop.services.editor.models import EditorResult
from pini_desktop.services.editor.validation import MoveValidator
from pini_desktop.services.scheduler_service import SchedulerService


class EditorService:
    """Facade for safe schedule editing.

    This service is intentionally independent from Qt. Views should call this
    service instead of modifying schedule_sessions directly.
    """

    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = Path(database_path)
        initialise_database(database_path=self.database_path)
        self.scheduler_service = SchedulerService(database_path=self.database_path)
        self.validator = MoveValidator(self.database_path)
        self.undo_stack = UndoStack()

    def validate_move(self, session_id: int, target_day: int, target_period: int) -> EditorResult:
        validation = self.validator.validate_move(session_id, target_day, target_period)
        if not validation.valid:
            return EditorResult.fail("Movimiento no válido.", warnings=validation.errors + validation.warnings)
        return EditorResult.ok("Movimiento válido.", warnings=validation.warnings)

    def move_session(self, session_id: int, target_day: int, target_period: int) -> EditorResult:
        validation = self.validator.validate_move(session_id, target_day, target_period)
        if not validation.valid:
            return EditorResult.fail("No se ha movido la sesión.", warnings=validation.errors + validation.warnings)

        before = self._score_placeholder()
        command = MoveSessionCommand(self.database_path, session_id, target_day, target_period)
        command.execute()
        self.undo_stack.push(command)
        after = self._score_placeholder()

        return EditorResult.ok(
            "Sesión movida correctamente.",
            warnings=validation.warnings,
            score_before=before,
            score_after=after,
            **self._affected_entities(session_id),
        )

    def swap_sessions(self, first_session_id: int, second_session_id: int) -> EditorResult:
        if first_session_id == second_session_id:
            return EditorResult.fail("No se puede intercambiar una sesión consigo misma.")

        before = self._score_placeholder()
        command = SwapSessionsCommand(self.database_path, first_session_id, second_session_id)
        try:
            command.execute()
        except ValueError as exc:
            return EditorResult.fail(str(exc))
        self.undo_stack.push(command)
        after = self._score_placeholder()

        affected = self._merge_affected(
            self._affected_entities(first_session_id),
            self._affected_entities(second_session_id),
        )
        return EditorResult.ok(
            "Sesiones intercambiadas correctamente.",
            score_before=before,
            score_after=after,
            **affected,
        )

    def undo(self) -> EditorResult:
        command = self.undo_stack.undo()
        if command is None:
            return EditorResult.fail("No hay acciones para deshacer.")
        return EditorResult.ok("Acción deshecha correctamente.")

    def redo(self) -> EditorResult:
        command = self.undo_stack.redo()
        if command is None:
            return EditorResult.fail("No hay acciones para rehacer.")
        return EditorResult.ok("Acción rehecha correctamente.")

    def list_sessions(self):
        return self.scheduler_service.list_sessions()

    def _score_placeholder(self) -> float | None:
        # Future 35.1A blocks will connect this to the optimizer score.
        return None

    def _affected_entities(self, session_id: int) -> dict:
        session = next((item for item in self.scheduler_service.list_sessions() if item.id == session_id), None)
        if session is None:
            return {"affected_teachers": (), "affected_courses": (), "affected_rooms": ()}
        return {
            "affected_teachers": (session.teacher_id,) if session.teacher_id is not None else (),
            "affected_courses": (session.course_id,),
            "affected_rooms": (session.room_id,) if session.room_id is not None else (),
        }

    def _merge_affected(self, first: dict, second: dict) -> dict:
        return {
            "affected_teachers": tuple(sorted(set(first["affected_teachers"] + second["affected_teachers"]))),
            "affected_courses": tuple(sorted(set(first["affected_courses"] + second["affected_courses"]))),
            "affected_rooms": tuple(sorted(set(first["affected_rooms"] + second["affected_rooms"]))),
        }
