# Commit 0002 - Desktop Foundation

Este commit añade la primera aplicación gráfica de Pini.

## Incluye

- Aplicación PySide6.
- Ventana principal.
- Menús.
- Barra de estado.
- Pantalla inicial.
- Base SQLite inicial creada automáticamente en `~/.pini/pini.db`.

## Ejecutar

```powershell
python -m pip install -e ".[dev]"
python -m pip install PySide6
$env:PYTHONPATH="apps/desktop;packages/core;packages/rule_engine;packages/scheduler;packages/persistence"
python -m pini_desktop
```
