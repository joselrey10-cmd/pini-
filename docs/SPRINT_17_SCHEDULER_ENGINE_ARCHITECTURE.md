# Sprint 17 - Arquitectura de motores de horario

Este sprint prepara Pini para evolucionar del generador básico a un solver real.

## Incluye

- Paquete `services/scheduler`.
- Dominio del motor:
  - `ScheduleAssignment`,
  - `SchedulePeriod`,
  - `SchedulePlacement`,
  - `ScheduleGenerationResult`.
- `SchedulerRepository`.
- `BasicSchedulerEngine`.
- Placeholder `OrToolsSchedulerEngine`.
- `SchedulerService` simplificado como fachada.
- Test de arquitectura.

## Importancia

A partir de aquí podremos introducir OR-Tools sin romper la interfaz ni las vistas ya creadas.
