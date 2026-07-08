# Sprint 35.2.5.4 - Integración visual del optimizador por zonas

Agrupa los paneles de optimización por zonas para integrarlos en la matriz del horario.

## Incluye

- `ZoneOptimizerTabs`
- `schedule_matrix_zone_patch.py`
- Integración preparada con:
  - `ZoneOptimizationPanel`
  - `ZoneIterativePanel`
- Conexión de `planApplied` con:
  - barra de estado,
  - historial visual,
  - recarga de matriz.
- Archivo de instrucciones para integración manual.
- Tests.

## Integración rápida

En `schedule_matrix_view.py`, después de crear `self.side_tabs`:

```python
from pini_desktop.ui.views.schedule_matrix_zone_patch import install_zone_optimizer_tabs

install_zone_optimizer_tabs(self)
```

## Resultado

El editor inteligente queda preparado para mostrar la optimización por zonas dentro de la matriz.
