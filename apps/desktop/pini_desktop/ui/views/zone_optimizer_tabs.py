from PySide6.QtWidgets import QTabWidget

from pini_desktop.ui.views.zone_iterative_panel import ZoneIterativePanel
from pini_desktop.ui.views.zone_optimization_panel import ZoneOptimizationPanel


class ZoneOptimizerTabs(QTabWidget):
    """Pestañas agrupadas para optimización por zonas."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.zone_optimization_panel = ZoneOptimizationPanel()
        self.zone_iterative_panel = ZoneIterativePanel()

        self.addTab(self.zone_optimization_panel, "Zona")
        self.addTab(self.zone_iterative_panel, "Zona avanzada")

    def connect_plan_applied(self, slot):
        self.zone_iterative_panel.planApplied.connect(slot)
