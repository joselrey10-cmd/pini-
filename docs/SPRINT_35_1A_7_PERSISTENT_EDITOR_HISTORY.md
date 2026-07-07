# Sprint 35.1A.7 - Historial persistente del editor

Guarda en base de datos las acciones del editor inteligente.

## Incluye

- Tabla `editor_history`
- `EditorHistoryService`
- Registro persistente de:
  - acción,
  - éxito/error,
  - mensajes,
  - avisos,
  - score anterior,
  - score nuevo,
  - fecha.
- `EditorHistoryPanel` ampliado:
  - cargar historial guardado,
  - limpiar vista,
  - borrar historial guardado.
- Tests del servicio.

## Siguiente paso

Versionado de horarios: guardar instantáneas completas antes/después de cambios importantes.
