from pini_desktop.ui.views.zone_optimizer_tabs import ZoneOptimizerTabs


def install_zone_optimizer_tabs(view) -> ZoneOptimizerTabs:
    tabs = ZoneOptimizerTabs(view)
    view.zone_optimizer_tabs = tabs

    if hasattr(view, "side_tabs"):
        view.side_tabs.addTab(tabs, "Optimización avanzada")

    tabs.connect_plan_applied(lambda result: _on_optimizer_applied(view, result))

    return tabs


def _on_optimizer_applied(view, result) -> None:
    applied = getattr(result, "applied", 0)
    failed = getattr(result, "failed", 0)
    text = f"Optimización aplicada. Correctas: {applied}. Fallidas: {failed}."

    if hasattr(view, "status_label"):
        view.status_label.setText(text)

    if hasattr(view, "history_panel"):
        view.history_panel.add_text(text)

    if hasattr(view, "load_matrix"):
        view.load_matrix()
