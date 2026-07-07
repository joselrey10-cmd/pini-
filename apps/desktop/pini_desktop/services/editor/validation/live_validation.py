from dataclasses import dataclass


@dataclass(frozen=True)
class LiveCellValidation:
    day: int
    period: int
    status: str
    message: str = ""

    @property
    def is_valid(self) -> bool:
        return self.status == "valid"


class LiveMoveValidator:
    """Validador ligero para colorear la matriz antes de ejecutar cambios.

    No sustituye a MoveValidator; solo da feedback visual rápido.
    """

    def validate_cell(self, source_session_id: int | None, target_session_id: int | None, day: int, period: int) -> LiveCellValidation:
        if source_session_id is None:
            return LiveCellValidation(day, period, "neutral", "No hay sesión seleccionada.")

        if target_session_id == source_session_id:
            return LiveCellValidation(day, period, "same", "Es la misma sesión.")

        if target_session_id is None:
            return LiveCellValidation(day, period, "valid", "Movimiento posible.")

        return LiveCellValidation(day, period, "swap", "Intercambio posible.")
