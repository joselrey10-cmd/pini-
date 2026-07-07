def test_schedule_dragdrop_table_can_be_imported():
    from pini_desktop.ui.views.schedule_dragdrop_table import ScheduleDragDropTable

    assert ScheduleDragDropTable is not None


def test_schedule_matrix_uses_dragdrop_table():
    from pini_desktop.ui.views.schedule_matrix_view import ScheduleMatrixView
    from pini_desktop.ui.views.schedule_dragdrop_table import ScheduleDragDropTable

    assert ScheduleMatrixView is not None
    assert ScheduleDragDropTable.MIME_TYPE == "application/x-pini-schedule-session"
