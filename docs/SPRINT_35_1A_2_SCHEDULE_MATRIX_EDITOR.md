# Sprint 35.1A.2 - Integración inicial del editor en la matriz

Este sprint conecta la vista de horarios con `EditorService` sin reescribir la interfaz.

## Incluye

- `ScheduleCell.id` para identificar sesiones reales.
- Eliminación de inicialización duplicada en `ScheduleViewService`.
- Metadatos internos en cada celda:
  - session_id,
  - day,
  - period.
- Menú contextual en la matriz:
  - marcar sesión,
  - mover sesión marcada a una celda vacía,
  - intercambiar con otra sesión,
  - cancelar selección.
- Botones:
  - Deshacer,
  - Rehacer.
- Integración con `EditorService`.
- Tests básicos de integración.

## Importante

Este sprint aún no activa Drag & Drop real. Es el paso previo: edición segura por menú contextual usando la infraestructura del editor.
