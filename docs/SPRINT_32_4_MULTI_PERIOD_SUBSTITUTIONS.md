# Sprint 32.4 - Sustituciones por tramos y varios periodos

Este sprint permite gestionar ausencias de varias sesiones seguidas.

## Incluye

- `MultiPeriodSubstitutionEngine`.
- `MultiPeriodSubstitutionPlan`.
- `PeriodSubstitutionPlan`.
- Detección de periodos cubiertos y no cubiertos.
- Adaptador Pini con:
  - `absences_from_teacher_periods`
  - `candidates_by_period`
- Servicio con:
  - `propose_range_from_pini`
  - `propose_for_absence_range`

## Utilidad

Pini puede proponer sustituciones para una ausencia parcial de mañana o varias horas consecutivas.
