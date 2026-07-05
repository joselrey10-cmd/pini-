# Sprint 9 - Horario general del centro

Este sprint añade la configuración temporal del centro.

## Incluye

- Tabla SQLite `timetable_settings`.
- Tabla SQLite `timetable_periods`.
- Servicio `TimetableService`.
- Vista `TimetableSettingsView`.
- Configuración de:
  - días lectivos,
  - sesiones diarias,
  - duración de sesión,
  - posición del recreo,
  - duración del recreo,
  - hora de inicio.
- Generación automática de periodos.
- Indicadores:
  - recreo después de periodo,
  - después del recreo.

## Importancia

Esta información será esencial para aplicar reglas como:

- Contextos después del recreo.
- Profesor no disponible.
- Máximo de sesiones diarias.
- Materias preferentemente a primera hora.
