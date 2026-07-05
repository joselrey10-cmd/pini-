from pathlib import Path

from pini_desktop.services.backup_service import BackupService
from pini_desktop.services.teacher_service import Teacher, TeacherService


def test_backup_and_restore(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    backup_dir = tmp_path / "backups"

    teacher_service = TeacherService(database_path=db)
    teacher_service.create_teacher(Teacher(None, "P01", "Ana", "García", "Primaria", 25, 5))

    service = BackupService(database_path=db, backup_dir=backup_dir)
    result = service.create_backup()

    assert result.created
    assert result.path.exists()
    assert len(service.list_backups()) == 1

    restored = service.restore_backup(result.path)
    assert restored.created
    assert db.exists()
