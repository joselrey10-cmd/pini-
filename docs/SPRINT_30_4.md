# Sprint 30.4 - Optimización de profesorado

Este sprint añade métricas específicas del profesorado al motor de optimización.

## Incluye

- `TeacherMetrics`
- `TeacherMetricsAnalyzer`
- Penalización de huecos por profesor.
- Penalización de últimas horas.
- Detección de exceso de carga diaria.
- Nuevo peso `teacher_compactness`.
- Informe ampliado por docente.
- Tests de métricas de profesorado.

## Objetivo

A partir de ahora Pini no solo busca horarios sin conflictos, sino horarios más cómodos para el profesorado.
