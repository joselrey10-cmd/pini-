import sqlite3
from pathlib import Path

from pini_desktop.services.editor.history.schedule_version_comparator import ScheduleVersionComparator
from pini_desktop.services.editor.history.schedule_version_service import ScheduleVersionService


def setup_db(path: Path):
    con = sqlite3.connect(path)
    con.executescript(
        """
        CREATE TABLE schedule_sessions(
            id INTEGER PRIMARY KEY,
            course_id INTEGER,
            subject_id INTEGER,
            teacher_id INTEGER,
            room_id INTEGER,
            day INTEGER,
            period INTEGER
        );
        INSERT INTO schedule_sessions VALUES(1,1,1,1,1,1,1);
        INSERT INTO schedule_sessions VALUES(2,1,1,1,1,1,2);
        """
    )
    con.commit()
    con.close()


def test_schedule_version_comparator_detects_moved_sessions(tmp_path: Path):
    db = tmp_path / "pini.db"
    setup_db(db)

    service = ScheduleVersionService(database_path=db)
    v1 = service.create_version("A")

    con = sqlite3.connect(db)
    con.execute("UPDATE schedule_sessions SET day=2, period=3 WHERE id=1")
    con.commit()
    con.close()

    v2 = service.create_version("B")

    comparison = ScheduleVersionComparator(database_path=db).compare(v1, v2)

    assert comparison.moved == 1
    assert comparison.added == 0
    assert comparison.removed == 0


def test_schedule_version_compare_panel_import():
    from pini_desktop.ui.views.schedule_version_compare_panel import ScheduleVersionComparePanel

    assert ScheduleVersionComparePanel is not None
