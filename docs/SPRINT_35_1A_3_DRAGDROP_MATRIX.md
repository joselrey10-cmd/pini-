# Sprint 35.1A.3 - Drag & Drop inicial en la matriz

Añade una tabla específica para horarios con soporte Drag & Drop interno.

## Incluye

- `ScheduleDragDropTable`
- MIME propio para sesiones de Pini
- Señales:
  - `sessionMoved(session_id, day, period)`
  - `sessionsSwapped(first_session_id, second_session_id)`
- Integración en `ScheduleMatrixView`
- Mantiene el menú contextual del sprint anterior
- Tests de importación

## Uso

- Arrastrar una sesión a una celda vacía: mover.
- Arrastrar una sesión sobre otra: intercambiar.

## Siguiente paso

Validación visual en vivo: colorear celdas válidas, conflictivas o mejorables durante la edición.
