# Sprint 10 - Validación del proyecto

Este sprint añade la validación previa del proyecto.

## Incluye

- Servicio `ProjectValidationService`.
- Modelo `ValidationIssue`.
- Vista `ProjectValidationView`.
- Acceso desde `Horarios > Validar proyecto`.
- Validaciones iniciales:
  - existe profesorado,
  - existen cursos,
  - existen materias,
  - existen aulas,
  - hay materias asignadas a cursos,
  - se han generado periodos,
  - las horas del profesorado son posibles con su máximo diario,
  - aviso si una materia por curso no tiene profesor preferente.
- Tests de proyecto vacío y proyecto mínimo completo.

## Importancia

Antes de generar horarios, Pini debe saber si el proyecto tiene datos suficientes y coherentes.
