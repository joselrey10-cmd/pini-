def test_schedule_matrix_view_imports_editor_service():
    from pini_desktop.ui.views.schedule_matrix_view import ScheduleMatrixView

    assert ScheduleMatrixView is not None


def test_schedule_cell_has_session_id_field():
    from pini_desktop.services.schedule_view_service import ScheduleCell

    cell = ScheduleCell(
        id=1,
        day=1,
        period=1,
        course_code="1A",
        subject_name="Lengua",
        teacher_name="Ana García",
        room_name="Aula 1",
    )

    assert cell.id == 1
