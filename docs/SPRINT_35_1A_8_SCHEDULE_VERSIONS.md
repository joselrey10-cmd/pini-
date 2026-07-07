# Sprint 35.1A.8 - Versionado de horarios

Permite guardar y restaurar versiones completas del horario.

## Incluye

- Tabla `schedule_versions`
- `ScheduleVersionService`
- Crear versión
- Listar versiones
- Restaurar versión
- Eliminar versión
- `ScheduleVersionsPanel`
- Integración como pestaña lateral en `ScheduleMatrixView`
- Tests

## Utilidad

Antes de hacer cambios importantes, el usuario puede guardar una versión del horario y volver a ella si el resultado no convence.
