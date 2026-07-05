# Sprint 29 - Comprobación y reparación automática

Añade una herramienta para detectar problemas de integración.

## Incluye

- Servicio `SelfCheckService`.
- Vista `SelfCheckView`.
- Menú `Herramientas > Comprobar y reparar Pini`.
- Acceso también desde `Ayuda`.
- Botón en pantalla de inicio.
- Comprobación de:
  - tablas principales,
  - vistas integradas en `main_window.py`.
- Reparación básica de base de datos llamando a `initialise_database()`.

## Utilidad

Ayuda a resolver problemas tras copiar sprints o si alguna tabla no existe.
