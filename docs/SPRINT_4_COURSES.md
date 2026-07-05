# Sprint 4 - Gestión de Cursos

Este sprint añade la gestión de cursos/grupos.

## Incluye

- Tabla SQLite `courses`.
- Servicio `CourseService`.
- Modelo `Course`.
- Vista `CoursesView`.
- Diálogo para crear y editar cursos.
- Acceso desde menú `Datos > Cursos`.
- Test CRUD completo.

## Ejecutar Pini

```powershell
$env:PYTHONPATH="apps/desktop;packages/core;packages/rule_engine;packages/scheduler;packages/persistence"
python -m pini_desktop
```
