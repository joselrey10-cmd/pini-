from pathlib import Path

from pini_desktop.services.center_config_service import CenterConfig, CenterConfigService
from pini_desktop.services.timetable_service import TimetableService, TimetableSettings


def test_center_config_save_and_load(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    service = CenterConfigService(database_path=db)

    config = CenterConfig(
        center_name="CEIP Tierra de Pinares",
        center_code="47001559",
        locality="Mojados",
        province="Valladolid",
        school_year="2026/2027",
        center_type="CEIP",
        stage="Primaria",
        school_day="Continua",
        start_time="09:00",
        sessions_per_day=6,
        session_duration_minutes=45,
        break_after_period=3,
        break_duration_minutes=30,
    )

    service.save_config(config)
    loaded = service.get_config()

    assert loaded.center_name == "CEIP Tierra de Pinares"
    assert loaded.center_code == "47001559"
    assert loaded.sessions_per_day == 6


def test_wizard_timetable_settings_can_be_generated(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    timetable = TimetableService(database_path=db)
    timetable.save_settings(TimetableSettings())
    timetable.save_generated_periods()

    assert len(timetable.list_periods()) == 30
