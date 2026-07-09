# Sprint 35.2.7.3.2 - Simulation Snapshot & Global Metrics

Añade snapshots, métricas globales, comparación y decisión básica para el simulador global.

## Incluye

- `GlobalMetrics`
- `GlobalMetricsCalculator`
- `SimulationSnapshot`
- `SimulationComparison`
- `SimulationComparisonService`
- `SimulationDecision`
- `SimulationDecisionEngine`
- `GlobalSimulationEngine`
- `GlobalSimulationResult`
- Tests

## Métricas iniciales

- sesiones totales,
- ventanas/huecos por profesor,
- huecos por curso,
- conflictos de aula,
- últimas horas,
- score global preliminar.

## Resultado

El simulador global ya puede comparar un horario virtual antes/después y decidir si una simulación mejora el centro.
