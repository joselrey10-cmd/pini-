from dataclasses import dataclass

from .models import ImportPackage


@dataclass(frozen=True)
class ImportResult:
    teachers: int = 0
    courses: int = 0
    subjects: int = 0
    rooms: int = 0
    warnings: tuple[str, ...] = ()


class EducaCyLImporter:
    def validate(self, package: ImportPackage) -> tuple[str, ...]:
        warnings = []
        if not package.teachers:
            warnings.append("No hay profesores en el paquete.")
        if not package.courses:
            warnings.append("No hay cursos en el paquete.")
        if not package.subjects:
            warnings.append("No hay materias en el paquete.")
        return tuple(warnings)

    def import_package(self, package: ImportPackage) -> ImportResult:
        return ImportResult(
            teachers=len(package.teachers),
            courses=len(package.courses),
            subjects=len(package.subjects),
            rooms=len(package.rooms),
            warnings=self.validate(package),
        )
