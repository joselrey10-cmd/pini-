# Sprint 8 - Disponibilidad del profesorado

Este sprint añade la matriz de disponibilidad docente.

## Incluye

- Tabla SQLite `teacher_availability`.
- Servicio `AvailabilityService`.
- Estados:
  - Disponible.
  - Preferente.
  - Evitar.
  - No disponible.
- Vista `TeacherAvailabilityView`.
- Acceso desde menú `Datos > Disponibilidad profesorado`.
- Test de matriz de disponibilidad.

## Uso

En la pantalla de disponibilidad:

- Selecciona profesor/a.
- Selecciona una o varias celdas.
- Pulsa:
  - `1`: Disponible.
  - `2`: Preferente.
  - `3`: Evitar.
  - `4`: No disponible.
- Pulsa guardar.
