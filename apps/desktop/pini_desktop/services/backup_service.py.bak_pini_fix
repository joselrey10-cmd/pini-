from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import shutil

from pini_desktop.config.settings import DATA_DIR, DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database


@dataclass(frozen=True)
class BackupResult:
    path: Path
    created: bool
    message: str


class BackupService:
    def __init__(self, database_path=DATABASE_PATH, backup_dir: Path | None = None):
        self.database_path = Path(database_path)
        self.backup_dir = backup_dir or (DATA_DIR / "backups")
        initialise_database()

    def create_backup(self, destination: str | Path | None = None) -> BackupResult:
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        destination_path = Path(destination) if destination else self.backup_dir / f"pini_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        destination_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.database_path.exists():
            return BackupResult(destination_path, False, "No existe base de datos para copiar.")

        shutil.copy2(self.database_path, destination_path)
        return BackupResult(destination_path, True, "Copia de seguridad creada correctamente.")

    def restore_backup(self, source: str | Path) -> BackupResult:
        source_path = Path(source)
        if not source_path.exists():
            return BackupResult(source_path, False, "No se encuentra el archivo de copia.")

        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, self.database_path)
        return BackupResult(self.database_path, True, "Copia restaurada correctamente.")

    def list_backups(self) -> list[Path]:
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        return sorted(self.backup_dir.glob("*.db"), reverse=True)
