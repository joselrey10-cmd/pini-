# Sprint 26 - Asistente de configuración del centro

Añade un asistente inicial para configurar el proyecto del centro.

## Incluye

- Servicio `CenterConfigService`.
- Tabla `center_config`.
- Vista `CenterWizardView`.
- Datos del centro:
  - nombre,
  - código,
  - localidad,
  - provincia,
  - curso escolar.
- Tipo de centro y etapa.
- Tipo de jornada.
- Configuración horaria.
- Generación automática de periodos.
- Integración en `main_window.py`.
- Acceso desde:
  - `Archivo > Asistente de configuración`,
  - `Centro > Asistente de configuración`,
  - pantalla de inicio.

## Importancia

Pini empieza a funcionar como aplicación profesional: al abrir un proyecto, el usuario tiene un asistente guiado.
