from __future__ import annotations

from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parent
BOOTSTRAP = ROOT / "apps" / "desktop" / "pini_desktop" / "database" / "bootstrap.py"
TEACHER_TEST = ROOT / "tests" / "desktop" / "test_teacher_service.py"


def backup(path: Path) -> None:
    bak = path.with_suffix(path.suffix + ".bak_pini_fix_v2")
    if path.exists() and not bak.exists():
        shutil.copy2(path, bak)


def patch_bootstrap_function() -> None:
    text = BOOTSTRAP.read_text(encoding="utf-8")

    pattern = re.compile(
        r"def initialise_database\(.*?\) -> None:\n"
        r".*?connection\.close\(\)\n",
        re.DOTALL,
    )

    replacement = """def initialise_database(database_path=None) -> None:
    target_path = database_path or DATABASE_PATH
    Path(target_path).parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(target_path)
    try:
        connection.executescript(SCHEMA)
        connection.execute(
            "INSERT OR REPLACE INTO app_metadata(key, value) VALUES(?, ?)",
            ("version", "0.1.0"),
        )
        connection.commit()
    finally:
        connection.close()
"""

    if not pattern.search(text):
        raise RuntimeError("No he podido localizar completa la función initialise_database en bootstrap.py")

    new_text = pattern.sub(replacement, text, count=1)
    backup(BOOTSTRAP)
    BOOTSTRAP.write_text(new_text, encoding="utf-8")
    print(f"OK reparado bootstrap.py: {BOOTSTRAP}")


def patch_teacher_test() -> None:
    if not TEACHER_TEST.exists():
        print("AVISO: no encuentro test_teacher_service.py")
        return

    fixed = """from pathlib import Path

from pini_desktop.database.bootstrap import initialise_database
from pini_desktop.services.teacher_service import Teacher, TeacherService


def test_teacher_crud(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    initialise_database(database_path=db)
    service = TeacherService(database_path=db)

    teacher_id = service.create_teacher(
        Teacher(
            id=None,
            code="P01",
            name="Ana",
            surname="García",
            speciality="Primaria",
            weekly_hours=25,
            max_daily_sessions=5,
        )
    )

    teachers = service.list_teachers()
    assert len(teachers) == 1
    assert teachers[0].id == teacher_id
    assert teachers[0].code == "P01"

    service.update_teacher(
        Teacher(
            id=teacher_id,
            code="P01",
            name="Ana",
            surname="García López",
            speciality="Primaria",
            weekly_hours=24,
            max_daily_sessions=5,
        )
    )
    assert service.list_teachers()[0].surname == "García López"

    service.delete_teacher(teacher_id)
    assert service.list_teachers() == []
"""
    backup(TEACHER_TEST)
    TEACHER_TEST.write_text(fixed, encoding="utf-8")
    print(f"OK reparado test_teacher_service.py: {TEACHER_TEST}")


def main() -> None:
    print("=== Reparación v2 PiniPlanner ===")
    patch_bootstrap_function()
    patch_teacher_test()
    print()
    print("Ahora ejecuta:")
    print("python -m pytest tests/desktop/test_teacher_service.py -v")


if __name__ == "__main__":
    main()
