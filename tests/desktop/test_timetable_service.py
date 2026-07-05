from pathlib import Path

from pini_desktop.services.timetable_service import TimetableService, TimetableSettings


def test_timetable_generates_periods(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    service = TimetableService(database_path=db)

    settings = TimetableSettings(
        working_days=5,
        sessions_per_day=6,
        session_duration_minutes=45,
        break_after_period=3,
        break_duration_minutes=30,
        start_time="09:00",
    )

    periods = service.generate_periods(settings)

    assert len(periods) == 30
    assert periods[0].start_time == "09:00"
    assert periods[0].end_time == "09:45"
    assert periods[2].is_break_after is True
    assert periods[3].is_after_break is True
    assert periods[3].start_time == "11:45"


def test_timetable_saves_generated_periods(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    service = TimetableService(database_path=db)

    service.save_settings(TimetableSettings())
    service.save_generated_periods()

    assert len(service.list_periods()) == 30
