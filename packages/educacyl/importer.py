from dataclasses import dataclass

from .models import ImportPackage
from .validator import ImportPackageValidator, ImportValidationReport


@dataclass(frozen=True)
class ImportResult:
    teachers: int = 0
    courses: int = 0
    subjects: int = 0
    rooms: int = 0
    warnings: tuple[str, ...] = ()
    validation_report: ImportValidationReport | None = None


class EducaCyLImporter:
    def __init__(self):
        self.validator = ImportPackageValidator()

    def validate(self, package: ImportPackage) -> tuple[str, ...]:
        report = self.validator.validate(package)
        return tuple(issue.message for issue in report.issues if issue.severity in {"WARNING", "ERROR"})

    def import_package(self, package: ImportPackage) -> ImportResult:
        report = self.validator.validate(package)
        warnings = tuple(issue.message for issue in report.issues if issue.severity in {"WARNING", "ERROR"})
        return ImportResult(
            teachers=len(package.teachers),
            courses=len(package.courses),
            subjects=len(package.subjects),
            rooms=len(package.rooms),
            warnings=warnings,
            validation_report=report,
        )
