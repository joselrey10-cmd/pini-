# Sprint 35.1A.1 - Infraestructura del Editor Inteligente

Este sprint crea la primera capa real del editor inteligente, integrada en la arquitectura `pini_desktop`.

## Incluye

- `apps/desktop/pini_desktop/services/editor/`
- `EditorService`
- `EditorResult`
- `MoveSessionCommand`
- `SwapSessionsCommand`
- `UndoStack`
- `MoveValidator`
- Tests de movimiento, intercambio y undo/redo.

## Decisión de arquitectura

No se crea `packages/editor`. El editor vive dentro de `pini_desktop.services.editor` porque trabaja directamente con la base SQLite y con los servicios de escritorio.

## Siguiente paso

35.1A.2 integrará esta capa con `ScheduleMatrixView` para preparar Drag & Drop y acciones de edición desde la interfaz.
