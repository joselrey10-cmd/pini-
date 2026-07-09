# Pack correctivo PiniPlanner v2

Este pack repara el error:

`IndentationError: unexpected indent` en `bootstrap.py`, línea 129.

## Uso

1. Copia `fix_pini_tests_v2.py` en:

   `C:\Proyectos\pini_initial_commit`

2. Ejecuta:

   `python fix_pini_tests_v2.py`

3. Después ejecuta:

   `python -m pytest tests/desktop/test_teacher_service.py -v`
