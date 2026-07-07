# Sprint 35.1A.9 - Optimización local inteligente

Añade análisis local después de movimientos o intercambios.

## Incluye

- `LocalOptimizationService`
- `LocalOptimizationSuggestion`
- `LocalOptimizationResult`
- `LocalOptimizationPanel`
- Nueva pestaña lateral `Mejoras`
- Análisis según score:
  - mejora: conservar cambio,
  - empeora: revisar zona afectada,
  - igual: buscar mejora local,
  - sin score: inspeccionar impacto.
- Tests.

## Siguiente paso

Convertir las sugerencias en acciones aplicables directamente desde el panel.
