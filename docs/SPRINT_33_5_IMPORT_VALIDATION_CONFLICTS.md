# Sprint 33.5 - Validación y resolución de conflictos

Añade validación previa y planes de resolución antes de aplicar importaciones.

## Incluye

- `ImportPackageValidator`
- `ImportValidationIssue`
- `ImportValidationReport`
- Detección de:
  - códigos duplicados,
  - campos obligatorios vacíos,
  - configuración incoherente.
- `ImportConflictResolver`
- `ConflictResolutionPolicy`
- `ConflictResolutionPlan`
- Previsualización de acciones:
  - altas,
  - cambios,
  - eliminaciones omitidas o aplicadas.
- Tests.

## Utilidad

Pini puede avisar antes de sincronizar y evita aplicar eliminaciones peligrosas por defecto.
