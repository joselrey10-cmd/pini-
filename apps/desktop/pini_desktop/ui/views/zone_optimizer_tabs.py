from PySide6.QtWidgets import QTabWidget

from pini_desktop.ui.views.sequence_optimizer_panel import SequenceOptimizerPanel
from pini_desktop.ui.views.zone_iterative_panel import ZoneIterativePanel
from pini_desktop.ui.views.zone_optimization_panel import ZoneOptimizationPanel


class ZoneOptimizerTabs(QTabWidget):
    """Pestañas agrupadas para optimización por zonas y cadenas."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.zone_optimization_panel = ZoneOptimizationPanel()
        self.zone_iterative_panel = ZoneIterativePanel()
        self.sequence_optimizer_panel = SequenceOptimizerPanel()

        self.addTab(self.zone_optimization_panel, "Zona")
        self.addTab(self.zone_iterative_panel, "Zona avanzada")
        self.addTab(self.sequence_optimizer_panel, "Cadenas IA")

    def connect_plan_applied(self, slot):
        self.zone_iterative_panel.planApplied.connect(slot)
        self.sequence_optimizer_panel.sequenceApplied.connect(slot)
