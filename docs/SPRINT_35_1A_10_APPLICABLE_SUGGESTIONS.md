# Sprint 35.1A.10 - Sugerencias aplicables

Permite que el panel de optimización local prepare sugerencias aplicables.

## Incluye

- `EditorSuggestionService`
- `SuggestionApplyResult`
- Soporte para sugerencias tipo:
  - `move`
  - `swap`
- Botón `Aplicar sugerencia seleccionada`
- Señal `suggestionApplied`
- Integración con `ScheduleMatrixView`
- Tests

## Importante

Las sugerencias actuales siguen siendo principalmente informativas. Este sprint deja preparada la infraestructura para que los siguientes motores generen acciones reales.
