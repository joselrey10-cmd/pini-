import sqlite3
from dataclasses import dataclass
from pathlib import Path

from .base_command import EditorCommand


@dataclass
class SwapSessionsCommand(EditorCommand):
    database_path: Path | str
    first_session_id: int
    second_session_id: int

    name = "swap_sessions"

    def __post_init__(self):
        self._previous_positions: tuple[tuple[int, int], tuple[int, int]] | None = None

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def execute(self):
        if self.first_session_id == self.second_session_id:
            return

        connection = self._connect()
        try:
            rows = connection.execute(
                "SELECT id, day, period FROM schedule_sessions WHERE id IN (?, ?)",
                (self.first_session_id, self.second_session_id),
            ).fetchall()
            positions = {int(row["id"]): (int(row["day"]), int(row["period"])) for row in rows}
            if self.first_session_id not in positions or self.second_session_id not in positions:
                raise ValueError("No se han encontrado las dos sesiones para intercambiar.")

            first_position = positions[self.first_session_id]
            second_position = positions[self.second_session_id]

            if self._previous_positions is None:
                self._previous_positions = (first_position, second_position)

            connection.execute(
                "UPDATE schedule_sessions SET day=?, period=? WHERE id=?",
                (second_position[0], second_position[1], self.first_session_id),
            )
            connection.execute(
                "UPDATE schedule_sessions SET day=?, period=? WHERE id=?",
                (first_position[0], first_position[1], self.second_session_id),
            )
            connection.commit()
        finally:
            connection.close()

    def undo(self):
        if self._previous_positions is None:
            return
        first_position, second_position = self._previous_positions
        connection = self._connect()
        try:
            connection.execute(
                "UPDATE schedule_sessions SET day=?, period=? WHERE id=?",
                (first_position[0], first_position[1], self.first_session_id),
            )
            connection.execute(
                "UPDATE schedule_sessions SET day=?, period=? WHERE id=?",
                (second_position[0], second_position[1], self.second_session_id),
            )
            connection.commit()
        finally:
            connection.close()
