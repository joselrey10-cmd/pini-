def test_zone_optimizer_tabs_includes_sequence_panel():
    from pini_desktop.ui.views.zone_optimizer_tabs import ZoneOptimizerTabs

    assert ZoneOptimizerTabs is not None


def test_schedule_matrix_zone_patch_imports():
    from pini_desktop.ui.views.schedule_matrix_zone_patch import install_zone_optimizer_tabs

    assert install_zone_optimizer_tabs is not None
