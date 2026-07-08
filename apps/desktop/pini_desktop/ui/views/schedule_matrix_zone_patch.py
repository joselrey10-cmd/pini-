"""Ayudante de integración para ScheduleMatrixView.

Este módulo permite añadir los paneles de optimización por zonas sin duplicar
la lógica de los paneles. Si la vista principal ya tiene `side_tabs`, basta con
llamar a `install_zone_optimizer_tabs(view)`.
"""

from pini_desktop.ui.views.zone_optimizer_tabs import ZoneOptimizerTabs


def install_zone_optimizer_tabs(view) -> ZoneOptimizerTabs:
    tabs = ZoneOptimizerTabs(view)
    view.zone_optimizer_tabs = tabs

    if hasattr(view, "side_tabs"):
        view.side_tabs.addTab(tabs, "Optimización por zonas")

    if hasattr(tabs.zone_iterative_panel, "planApplied"):
        tabs.zone_iterative_panel.planApplied.connect(lambda result: _on_zone_plan_applied(view, result))

    return tabs


def _on_zone_plan_applied(view, result) -> None:
    text = (
        f"Plan de zona aplicado. Correctas: {getattr(result, 'applied', 0)}. "
        f"Fallidas: {getattr(result, 'failed', 0)}."
    )

    if hasattr(view, "status_label"):
        view.status_label.setText(text)

    if hasattr(view, "history_panel"):
        view.history_panel.add_text(text)

    if hasattr(view, "load_matrix"):
        view.load_matrix()
