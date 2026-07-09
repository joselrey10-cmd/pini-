from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OptimizationRequest:
    scope: str          # session | teacher | course
    target_id: int


@dataclass(frozen=True)
class OptimizationResponse:
    success: bool
    summary: str
    result: object | None = None


class OptimizationOrchestrator:
    """
    Punto único de entrada para cualquier optimización.
    """

    def __init__(
        self,
        session_service=None,
        teacher_service=None,
        course_service=None,
    ):
        self.session_service = session_service
        self.teacher_service = teacher_service
        self.course_service = course_service

    def optimize(self, request: OptimizationRequest):

        if request.scope == "session":
            if self.session_service is None:
                return OptimizationResponse(
                    False,
                    "Servicio de sesión no disponible.",
                )

            result = self.session_service.optimize_session(
                request.target_id
            )

            return OptimizationResponse(
                True,
                "Optimización de sesión completada.",
                result,
            )

        if request.scope == "teacher":
            if self.teacher_service is None:
                return OptimizationResponse(
                    False,
                    "Servicio de profesor no disponible.",
                )

            result = self.teacher_service.optimize_teacher(
                request.target_id
            )

            return OptimizationResponse(
                True,
                "Optimización de profesor completada.",
                result,
            )

        if request.scope == "course":
            if self.course_service is None:
                return OptimizationResponse(
                    False,
                    "Servicio de curso no disponible.",
                )

            result = self.course_service.optimize_course(
                request.target_id
            )

            return OptimizationResponse(
                True,
                "Optimización de curso completada.",
                result,
            )

        return OptimizationResponse(
            False,
            "Ámbito de optimización desconocido.",
        )