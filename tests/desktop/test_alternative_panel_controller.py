from pini_desktop.ui.editor.alternative_panel_controller import (
    AlternativePanelController,
)


class FakePanel:
    def __init__(self):
        self.alternatives = None

    def set_alternatives(self, alternatives):
        self.alternatives = alternatives


class FakeEditorService:
    pass


def test_alternative_panel_controller_updates_panel():
    panel = FakePanel()
    controller = AlternativePanelController(panel, FakeEditorService())

    controller.on_session_selected(1)

    assert panel.alternatives is not None