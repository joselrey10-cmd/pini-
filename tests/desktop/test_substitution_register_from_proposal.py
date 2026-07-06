def test_substitution_view_and_registry_view_can_be_imported():
    from pini_desktop.ui.views.substitution_view import SubstitutionView
    from pini_desktop.ui.views.substitution_registry_view import SubstitutionRegistryView

    assert SubstitutionView is not None
    assert SubstitutionRegistryView is not None
