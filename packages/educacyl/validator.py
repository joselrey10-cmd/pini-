from dataclasses import dataclass
from typing import Literal

from .models import ImportPackage


Severity = Literal["INFO", "WARNING", "ERROR"]


@dataclass(frozen=True)
class ImportValidationIssue:
    severity: Severity
    entity: str
    code: str
    message: str
    suggestion: str = ""


@dataclass(frozen=True)
class ImportValidationReport:
    issues: tuple[ImportValidationIssue, ...] = ()

    @property
    def has_errors(self) -> bool:
        return any(issue.severity == "ERROR" for issue in self.issues)

    @property
    def has_warnings(self) -> bool:
        return any(issue.severity == "WARNING" for issue in self.issues)

    @property
    def total(self) -> int:
        return len(self.issues)


class ImportPackageValidator:
    def validate(self, package: ImportPackage) -> ImportValidationReport:
        issues = []
        issues.extend(self._validate_entities("teacher", package.teachers, ["code", "name", "surname"]))
        issues.extend(self._validate_entities("course", package.courses, ["code", "stage", "group_name"]))
        issues.extend(self._validate_entities("subject", package.subjects, ["code", "name"]))
        issues.extend(self._validate_entities("room", package.rooms, ["code", "name"]))
        issues.extend(self._validate_configuration(package))
        return ImportValidationReport(tuple(issues))

    def _validate_entities(self, entity: str, items, required_fields: list[str]):
        issues = []
        seen = set()

        for item in items:
            code = getattr(item, "code", "")

            if not code:
                issues.append(
                    ImportValidationIssue(
                        "ERROR",
                        entity,
                        "",
                        f"{entity}: falta código.",
                        "Completa el código antes de importar.",
                    )
                )
                continue

            if code in seen:
                issues.append(
                    ImportValidationIssue(
                        "ERROR",
                        entity,
                        code,
                        f"{entity}: código duplicado {code}.",
                        "Cada elemento debe tener un código único.",
                    )
                )
            seen.add(code)

            for field in required_fields:
                value = getattr(item, field, "")
                if value is None or str(value).strip() == "":
                    issues.append(
                        ImportValidationIssue(
                            "WARNING",
                            entity,
                            code,
                            f"{entity} {code}: campo vacío '{field}'.",
                            "Revisa si el campo debe completarse.",
                        )
                    )

        return issues

    def _validate_configuration(self, package: ImportPackage):
        issues = []
        config = package.configuration
        if config is None:
            issues.append(
                ImportValidationIssue(
                    "INFO",
                    "configuration",
                    "",
                    "No se incluye configuración del centro.",
                    "Se mantendrá la configuración actual de Pini.",
                )
            )
            return issues

        if config.sessions_per_day <= 0:
            issues.append(
                ImportValidationIssue(
                    "ERROR",
                    "configuration",
                    config.center_code,
                    "El número de sesiones por día debe ser positivo.",
                    "Corrige el campo sesiones_dia.",
                )
            )

        if config.break_after_period >= config.sessions_per_day:
            issues.append(
                ImportValidationIssue(
                    "WARNING",
                    "configuration",
                    config.center_code,
                    "El recreo está configurado después de la última sesión o demasiado tarde.",
                    "Revisa recreo_tras y sesiones_dia.",
                )
            )

        return issues
