# Pini

Pini es un proyecto para crear una aplicación profesional de generación, edición y gestión de horarios escolares.

## Primer commit de producción

Incluye:

- Estructura del repositorio.
- Paquete ejecutable con `python -m pini_core`.
- Módulo inicial `pini_rule_engine`.
- API del Rule Engine.
- Persistencia SQLite básica.
- Tests iniciales.

## Reglas iniciales CEIP Tierra de Pinares

- Máximo general de sesiones consecutivas por área: **1**.
- Excepción: **Inglés de 4.º a 6.º**, máximo **2 sesiones consecutivas**.
- Contextos: **después del recreo**.

## Ejecutar

```bash
python -m pini_core
```

## Tests

```bash
python -m pytest
```
