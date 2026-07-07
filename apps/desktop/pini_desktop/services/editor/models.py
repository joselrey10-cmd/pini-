from dataclasses import dataclass, field


@dataclass(frozen=True)
class EditorResult:
    success: bool
    messages: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    score_before: float | None = None
    score_after: float | None = None
    affected_teachers: tuple[int, ...] = ()
    affected_courses: tuple[int, ...] = ()
    affected_rooms: tuple[int, ...] = ()

    @classmethod
    def ok(cls, message: str = "Operación realizada correctamente.", **kwargs):
        return cls(success=True, messages=(message,), **kwargs)

    @classmethod
    def fail(cls, message: str, warnings: tuple[str, ...] = (), **kwargs):
        return cls(success=False, messages=(message,), warnings=warnings, **kwargs)
