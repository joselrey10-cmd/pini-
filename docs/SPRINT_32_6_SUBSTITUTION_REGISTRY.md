# Sprint 32.6 - Registro de sustituciones

Este sprint añade persistencia para las sustituciones seleccionadas.

## Incluye

- Tabla `substitution_records`.
- Servicio `SubstitutionRegistryService`.
- Estados:
  - `PLANNED`
  - `DONE`
  - `CANCELLED`
- Vista `SubstitutionRegistryView`.
- Marcar sustitución como realizada.
- Cancelar sustitución.
- Test del registro.

## Siguiente paso

Conectar la vista de propuestas para que al seleccionar una propuesta se registre automáticamente.
