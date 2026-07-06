from __future__ import annotations

from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parent

BOOTSTRAP = ROOT / "apps" / "desktop" / "pini_desktop" / "database" / "bootstrap.py"
SERVICES_DIR = ROOT / "apps" / "desktop" / "pini_desktop" / "services"
TEACHER_TEST = ROOT / "tests" / "desktop" / "test_teacher_service.py"


def backup(path: Path) -> None:
    bak = path.with_suffix(path.suffix + ".bak_pini_fix")
    if path.exists() and not bak.exists():
        shutil.copy2(path, bak)


def write_if_changed(path: Path, text: str) -> bool:
    old = path.read_text(encoding="utf-8")
    if old == text:
        return False
    backup(path)
    path.write_text(text, encoding="utf-8")
    return True


def patch_bootstrap() -> bool:
    if not BOOTSTRAP.exists():
        print(f"ERROR: no encuentro {BOOTSTRAP}")
        return False

    text = BOOTSTRAP.read_text(encoding="utf-8")

    text = text.replace(
        "def initialise_database() -> None:",
        "def initialise_database(database_path=None) -> None:",
    )

    text = text.replace(
        "connection = sqlite3.connect(DATABASE_PATH)",
        "target_path = database_path or DATABASE_PATH\n    connection = sqlite3.connect(target_path)",
    )

    text = re.sub(
        r"target_path = database_path or DATABASE_PATH\s*\n\s*target_path = database_path or DATABASE_PATH\s*\n\s*connection = sqlite3\.connect\(target_path\)",
        "target_path = database_path or DATABASE_PATH\n    connection = sqlite3.connect(target_path)",
        text,
    )

    changed = write_if_changed(BOOTSTRAP, text)
    print(("OK modificado: " if changed else "OK ya estaba bien: ") + str(BOOTSTRAP))
    return True


def patch_services() -> int:
    if not SERVICES_DIR.exists():
        print(f"AVISO: no encuentro {SERVICES_DIR}")
        return 0

    changed_count = 0

    for path in sorted(SERVICES_DIR.glob("*_service.py")):
        text = path.read_text(encoding="utf-8")
        original = text

        if "database_path" not in text:
            continue

        if "from pini_desktop.database.bootstrap import initialise_database" not in text:
            lines = text.splitlines()
            insert_at = 0
            while insert_at < len(lines) and (
                lines[insert_at].startswith("from ")
                or lines[insert_at].startswith("import ")
                or lines[insert_at].strip() == ""
            ):
                insert_at += 1
            lines.insert(insert_at, "from pini_desktop.database.bootstrap import initialise_database")
            text = "\n".join(lines) + ("\n" if original.endswith("\n") else "")

        patterns = [
            r"(self\.database_path\s*=\s*database_path\s*\n)(?!\s*initialise_database\(database_path=self\.database_path\))",
            r"(self\.database_path\s*=\s*Path\(database_path\)\s*\n)(?!\s*initialise_database\(database_path=self\.database_path\))",
        ]

        for pattern in patterns:
            text = re.sub(
                pattern,
                r"\1        initialise_database(database_path=self.database_path)\n",
                text,
                count=1,
            )

        if text != original:
            backup(path)
            path.write_text(text, encoding="utf-8")
            changed_count += 1
            print(f"OK modificado: {path}")

    if changed_count == 0:
        print("AVISO: no he modificado servicios. Puede que ya estén correctos o que usen otra estructura.")
    return changed_count


def repair_teacher_test() -> bool:
    if not TEACHER_TEST.exists():
        print(f"AVISO: no encuentro {TEACHER_TEST}")
        return False

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

    changed = write_if_changed(TEACHER_TEST, fixed)
    print(("OK reparado: " if changed else "OK ya estaba bien: ") + str(TEACHER_TEST))
    return True


def main() -> None:
    print("=== Pack correctivo PiniPlanner ===")
    print(f"Proyecto detectado en: {ROOT}")
    patch_bootstrap()
    patch_services()
    repair_teacher_test()

    print()
    print("Ahora ejecuta:")
    print("python -m pytest tests/desktop/test_teacher_service.py -v")
    print()
    print("Si pasa, ejecuta:")
    print("python -m pytest tests/desktop -v")


if __name__ == "__main__":
    main()
