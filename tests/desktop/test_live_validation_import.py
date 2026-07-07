def test_live_validation_import():
    from pini_desktop.services.editor.validation.live_validation import LiveMoveValidator

    validator = LiveMoveValidator()
    result = validator.validate_cell(source_session_id=1, target_session_id=None, day=1, period=1)

    assert result.status == "valid"
    assert result.is_valid


def test_live_validation_swap_status():
    from pini_desktop.services.editor.validation.live_validation import LiveMoveValidator

    validator = LiveMoveValidator()
    result = validator.validate_cell(source_session_id=1, target_session_id=2, day=1, period=1)

    assert result.status == "swap"
