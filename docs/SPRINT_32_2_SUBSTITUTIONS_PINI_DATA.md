# Sprint 32.2 - Sustituciones conectadas con datos de Pini

Este sprint conecta el motor de sustituciones con la base de datos real.

## Incluye

- `PiniSubstitutionDataAdapter`.
- Lectura de ausencia desde `schedule_sessions`.
- Lectura de candidatos desde `teachers`.
- Comprobación de si un docente está ocupado.
- Lectura de disponibilidad:
  - `AVAILABLE`
  - `PREFERRED`
  - `AVOID`
  - `FORBIDDEN`
- Servicio `PiniSubstitutionService` en la app de escritorio.
- Tests con base SQLite temporal.

## Utilidad

Pini ya puede proponer sustitutos partiendo de datos reales del horario generado.
