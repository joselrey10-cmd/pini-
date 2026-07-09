from pini_desktop.ui.editor.alternative_panel_integration import (
    AlternativePanelIntegration,
)


class FakeSignal:
    def __init__(self):
        self.callback = None

    def connect(self, callback):
        self.callback = callback


class FakePanel:
    def __init__(self):
        self.apply_requested = FakeSignal()

    def set_alternatives(self, alternatives):
        self.alternatives = alternatives


class FakeEditorView:
    def __init__(self):
        self.alternative_panel = FakePanel()
        self.session_selected = FakeSignal()


class FakeEditorService:
    pass


def test_alternative_panel_integration_enables_controller():
    view = FakeEditorView()
    service = FakeEditorService()

    integration = AlternativePanelIntegration(view, service)

    assert integration.is_enabled()
    assert view.session_selected.callback is not None