# Sprint 33.4 - Sincronización incremental

Añade comparación entre la importación anterior y la nueva.

## Incluye

- `ImportPackageDiffer`
- `DiffItem`
- `ImportDiff`
- `ImportPackageStore`
- Guardado del último paquete importado.
- Detección de:
  - altas,
  - modificaciones,
  - eliminaciones.
- `preview_diff_from_file`.
- Resumen desktop con cambios.

## Utilidad

Antes de importar datos, Pini puede informar de qué cambiará respecto a la última sincronización.
