# Sprint 16 - Generador sensible a reglas dinámicas

Este sprint empieza a conectar las reglas dinámicas con el generador.

## Incluye

- Servicio `RuleRuntimeService`.
- El generador básico lee reglas activas.
- Reglas aplicadas inicialmente:
  - `No permitir franja`.
  - `Preferir franja`.
  - `Evitar franja`.
  - `Después del recreo`.
  - `Aula obligatoria`.
- Tests de interpretación de reglas.

## Importante

Sigue sin ser el solver OR-Tools definitivo, pero ya empieza a usar condicionantes configurables desde la aplicación.
