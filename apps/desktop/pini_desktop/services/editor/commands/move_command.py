import sqlite3
from dataclasses import dataclass
from pathlib import Path

from .base_command import EditorCommand


@dataclass
class MoveSessionCommand(EditorCommand):
    database_path: Path | str
    session_id: int
    target_day: int
    target_period: int

    name = "move_session"

    def __post_init__(self):
        self._previous_position: tuple[int, int] | None = None

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def execute(self):
        connection = self._connect()
        try:
            row = connection.execute(
                "SELECT day, period FROM schedule_sessions WHERE id=?",
                (self.session_id,),
            ).fetchone()
            if row is None:
                raise ValueError(f"No existe la sesión {self.session_id}.")

            if self._previous_position is None:
                self._previous_position = (int(row["day"]), int(row["period"]))

            connection.execute(
                "UPDATE schedule_sessions SET day=?, period=? WHERE id=?",
                (self.target_day, self.target_period, self.session_id),
            )
            connection.commit()
        finally:
            connection.close()

    def undo(self):
        if self._previous_position is None:
            return
        connection = self._connect()
        try:
            connection.execute(
                "UPDATE schedule_sessions SET day=?, period=? WHERE id=?",
                (self._previous_position[0], self._previous_position[1], self.session_id),
            )
            connection.commit()
        finally:
            connection.close()
