# Sprint 31.2 - Recocido simulado

Este sprint añade un segundo algoritmo de optimización.

## Incluye

- `SimulatedAnnealingOptimizer`.
- `AnnealingResult`.
- Aceptación probabilística de movimientos peores.
- Temperatura inicial.
- Enfriamiento progresivo.
- Semilla para resultados reproducibles en tests.
- `SearchReport` ampliado con modo `annealing`.

## Importancia

El optimizador puede escapar de óptimos locales, algo esencial en horarios complejos.
