# Sprint 35.2.7.3.1 - Global Simulation Engine Core

Primer núcleo del simulador global del horario.

## Incluye

- `simulation/__init__.py`
- `virtual_schedule.py`
- `simulation_snapshot.py`
- `global_metrics.py`
- `simulation_comparison.py`
- `decision_engine.py`
- `global_simulation_engine.py`
- Tests de núcleo

## Qué aporta

Pini puede crear una copia virtual completa del horario, aplicar una secuencia de movimientos en memoria, calcular métricas globales, comparar antes/después y aceptar o rechazar la simulación sin tocar el horario real.

## Siguiente paso

Integrar este motor con el panel de cadenas IA para que las secuencias se validen por impacto global antes de aplicarse.
