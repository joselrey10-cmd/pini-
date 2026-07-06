# Sprint 34.3A - Núcleo común de evaluación por objetivos

Consolida el motor de optimización para que todos los criterios se calculen mediante objetivos independientes.

## Incluye

- `OptimizationObjective`
- `ObjectiveRegistry`
- `ScheduleEvaluator`
- `OptimizationEngine`
- `EvaluationScore`
- `ObjectiveScore`
- Objetivos iniciales:
  - restricciones,
  - compactación del profesorado,
  - distribución del alumnado,
  - calidad de aulas.
- Tests del núcleo.

## Utilidad

A partir de ahora se podrán añadir nuevos criterios de calidad creando una clase objetivo sin modificar el resto del motor.
