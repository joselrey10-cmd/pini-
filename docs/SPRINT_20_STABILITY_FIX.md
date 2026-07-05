# Sprint 20 - Reparación de estabilidad

Corrige dos errores detectados tras el Sprint 19.

## Corrige

- Restaura `bootstrap.py` completo con todas las tablas:
  - teachers,
  - courses,
  - subjects,
  - rooms,
  - course_subjects,
  - teacher_availability,
  - timetable_settings,
  - timetable_periods,
  - schedule_sessions,
  - dynamic_rules.
- Corrige `main_window.py` eliminando el uso incompatible de `RightSide`.

## Motivo

Algunos sprints anteriores podían dejar el esquema de base de datos incompleto si se copiaban parcialmente.
Este sprint vuelve a dejar la base estable.
