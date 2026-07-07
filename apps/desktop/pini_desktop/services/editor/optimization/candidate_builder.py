from dataclasses import dataclass


@dataclass(frozen=True)
class MoveCandidate:
    session_id: int
    day: int
    period: int
    title: str
    reason: str = ""


class CandidateBuilder:
    """Genera candidatos de movimiento alrededor de una sesión.

    Esta primera versión no modifica el horario. Solo propone celdas destino
    dentro de una ventana local de días y periodos.
    """

    def build_move_candidates(
        self,
        session_id: int,
        current_day: int,
        current_period: int,
        max_days: int = 5,
        max_periods: int = 6,
        radius: int = 2,
    ) -> tuple[MoveCandidate, ...]:
        candidates = []

        for day in range(1, max_days + 1):
            for period in range(1, max_periods + 1):
                if day == current_day and period == current_period:
                    continue

                distance = abs(day - current_day) + abs(period - current_period)
                if distance > radius:
                    continue

                candidates.append(
                    MoveCandidate(
                        session_id=session_id,
                        day=day,
                        period=period,
                        title=f"Mover a día {day}, periodo {period}",
                        reason="Candidato cercano a la posición actual.",
                    )
                )

        return tuple(candidates)

    def build_day_candidates(
        self,
        session_id: int,
        current_day: int,
        current_period: int,
        max_days: int = 5,
    ) -> tuple[MoveCandidate, ...]:
        candidates = []
        for day in range(1, max_days + 1):
            if day == current_day:
                continue
            candidates.append(
                MoveCandidate(
                    session_id=session_id,
                    day=day,
                    period=current_period,
                    title=f"Mover al mismo periodo del día {day}",
                    reason="Mantiene el periodo y cambia solo el día.",
                )
            )
        return tuple(candidates)
