import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MoveValidationResult:
    valid: bool
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()


class MoveValidator:
    def __init__(self, database_path):
        self.database_path = Path(database_path)

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def validate_move(self, session_id: int, target_day: int, target_period: int) -> MoveValidationResult:
        errors = []
        warnings = []

        if target_day < 1:
            errors.append("El día de destino debe ser mayor o igual que 1.")
        if target_period < 1:
            errors.append("El periodo de destino debe ser mayor o igual que 1.")
        if errors:
            return MoveValidationResult(False, tuple(errors), tuple(warnings))

        connection = self._connect()
        try:
            session = connection.execute(
                """
                SELECT id, course_id, teacher_id, room_id, day, period, locked
                FROM schedule_sessions
                WHERE id=?
                """,
                (session_id,),
            ).fetchone()
            if session is None:
                return MoveValidationResult(False, (f"No existe la sesión {session_id}.",), ())

            if int(session["locked"] or 0) == 1:
                return MoveValidationResult(False, ("La sesión está bloqueada y no se puede mover.",), ())

            rows = connection.execute(
                """
                SELECT id, course_id, teacher_id, room_id
                FROM schedule_sessions
                WHERE day=? AND period=? AND id<>?
                """,
                (target_day, target_period, session_id),
            ).fetchall()

            for row in rows:
                if int(row["course_id"]) == int(session["course_id"]):
                    errors.append("El grupo ya tiene otra sesión en ese periodo.")
                if session["teacher_id"] is not None and row["teacher_id"] == session["teacher_id"]:
                    errors.append("El profesor ya tiene otra sesión en ese periodo.")
                if session["room_id"] is not None and row["room_id"] == session["room_id"]:
                    errors.append("El aula ya está ocupada en ese periodo.")

            availability = self._teacher_availability(connection, session["teacher_id"], target_day, target_period)
            if availability == "FORBIDDEN":
                errors.append("El profesor no está disponible en ese periodo.")
            elif availability == "AVOID":
                warnings.append("El profesor tiene disponibilidad marcada como evitar en ese periodo.")

            return MoveValidationResult(not errors, tuple(dict.fromkeys(errors)), tuple(dict.fromkeys(warnings)))
        finally:
            connection.close()

    def _teacher_availability(self, connection, teacher_id, day: int, period: int) -> str:
        if teacher_id is None:
            return "AVAILABLE"
        row = connection.execute(
            "SELECT status FROM teacher_availability WHERE teacher_id=? AND day=? AND period=?",
            (teacher_id, day, period),
        ).fetchone()
        return row["status"] if row else "AVAILABLE"
