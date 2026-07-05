# Sprint 11 - Primer generador básico

Este sprint añade el primer generador de horario.

## Incluye

- Tabla SQLite `schedule_sessions`.
- Servicio `SchedulerService`.
- Vista `ScheduleView`.
- Botón `Generar horario básico`.
- Limpieza de horario generado.
- Visualización de sesiones generadas.
- Validación previa antes de generar.
- Respeta inicialmente:
  - un curso no se duplica en la misma franja,
  - un profesor no se duplica en la misma franja,
  - un aula no se duplica en la misma franja,
  - indisponibilidad `FORBIDDEN` del profesorado,
  - tipo de aula requerido cuando existe.

## Importante

Este no es todavía el solver definitivo con OR-Tools. Es el primer generador funcional para cerrar el circuito completo:

datos -> validación -> generación -> visualización.
