from dataclasses import dataclass
import sqlite3
from pathlib import Path

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database


@dataclass(frozen=True)
class SelfCheckItem:
    area: str
    status: str
    message: str


class SelfCheckService:
    REQUIRED_TABLES = [
        "teachers",
        "courses",
        "subjects",
        "rooms",
        "course_subjects",
        "teacher_availability",
        "timetable_settings",
        "timetable_periods",
        "schedule_sessions",
        "dynamic_rules",
        "center_config",
    ]

    REQUIRED_IMPORTS = [
        "BackupView",
        "CenterWizardView",
        "SchoolTemplateView",
        "DynamicRulesView",
        "ImportView",
        "ExportView",
    ]

    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = Path(database_path)
        initialise_database()

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def run_checks(self) -> list[SelfCheckItem]:
        items: list[SelfCheckItem] = []
        items.extend(self._check_database_tables())
        items.extend(self._check_main_window_imports())
        return items

    def repair_database(self) -> list[SelfCheckItem]:
        initialise_database()
        return self._check_database_tables()

    def _check_database_tables(self) -> list[SelfCheckItem]:
        items = []
        con = self._connect()
        try:
            rows = con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            tables = {row["name"] for row in rows}
        finally:
            con.close()

        for table in self.REQUIRED_TABLES:
            if table in tables:
                items.append(SelfCheckItem("Base de datos", "OK", f"Tabla correcta: {table}"))
            else:
                items.append(SelfCheckItem("Base de datos", "ERROR", f"Falta tabla: {table}"))

        return items

    def _check_main_window_imports(self) -> list[SelfCheckItem]:
        items = []
        main_window_path = Path(__file__).parents[1] / "ui" / "main_window.py"

        if not main_window_path.exists():
            return [SelfCheckItem("Interfaz", "ERROR", "No se encuentra main_window.py")]

        content = main_window_path.read_text(encoding="utf-8")

        for name in self.REQUIRED_IMPORTS:
            if name in content:
                items.append(SelfCheckItem("Interfaz", "OK", f"Vista integrada: {name}"))
            else:
                items.append(SelfCheckItem("Interfaz", "AVISO", f"No aparece integrada la vista: {name}"))

        return items
