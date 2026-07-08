def test_zone_optimizer_tabs_can_be_imported():
    from pini_desktop.ui.views.zone_optimizer_tabs import ZoneOptimizerTabs

    assert ZoneOptimizerTabs is not None


def test_schedule_matrix_zone_patch_can_be_imported():
    from pini_desktop.ui.views.schedule_matrix_zone_patch import install_zone_optimizer_tabs

    assert install_zone_optimizer_tabs is not None
