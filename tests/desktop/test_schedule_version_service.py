import sqlite3
from pathlib import Path

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
        """
    )
    con.commit()
    con.close()


def test_schedule_version_create_list_restore_delete(tmp_path: Path):
    db = tmp_path / "pini.db"
    setup_db(db)

    service = ScheduleVersionService(database_path=db)
    version_id = service.create_version("Inicial", "Prueba")

    versions = service.list_versions()
    assert len(versions) == 1
    assert versions[0].id == version_id
    assert versions[0].sessions_count == 1

    con = sqlite3.connect(db)
    con.execute("UPDATE schedule_sessions SET day=2 WHERE id=1")
    con.commit()
    con.close()

    service.restore_version(version_id)

    con = sqlite3.connect(db)
    row = con.execute("SELECT day FROM schedule_sessions WHERE id=1").fetchone()
    con.close()

    assert row[0] == 1

    service.delete_version(version_id)
    assert service.list_versions() == []
