# Sprint 35.2.6.3 - Integración visual del motor de cadenas

Integra el panel de cadenas inteligentes dentro del bloque de optimización avanzada.

## Incluye

- `ZoneOptimizerTabs` ampliado.
- Nueva pestaña `Cadenas IA`.
- Integración con:
  - `ZoneOptimizationPanel`
  - `ZoneIterativePanel`
  - `SequenceOptimizerPanel`
- Conexión común de aplicación de planes/cadenas.
- Actualización de `schedule_matrix_zone_patch.py`.
- Instrucciones de integración manual.
- Tests.

## Resultado

La matriz del horario puede acceder a:
- optimización simple por zona,
- búsqueda iterativa,
- cadenas multi-movimiento.
