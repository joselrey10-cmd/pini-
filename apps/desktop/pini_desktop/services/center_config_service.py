import sqlite3
from dataclasses import dataclass

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database


CREATE_SQL = """
CREATE TABLE IF NOT EXISTS center_config(
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


@dataclass(frozen=True)
class CenterConfig:
    center_name: str = "CEIP Tierra de Pinares"
    center_code: str = ""
    locality: str = "Mojados"
    province: str = "Valladolid"
    school_year: str = "2026/2027"
    center_type: str = "CEIP"
    stage: str = "Primaria"
    school_day: str = "Continua"
    start_time: str = "09:00"
    sessions_per_day: int = 6
    session_duration_minutes: int = 45
    break_after_period: int = 3
    break_duration_minutes: int = 30


class CenterConfigService:
    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        initialise_database()
        self._ensure_table()

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _ensure_table(self) -> None:
        con = self._connect()
        try:
            con.executescript(CREATE_SQL)
            con.commit()
        finally:
            con.close()

    def save_config(self, config: CenterConfig) -> None:
        data = {
            "center_name": config.center_name,
            "center_code": config.center_code,
            "locality": config.locality,
            "province": config.province,
            "school_year": config.school_year,
            "center_type": config.center_type,
            "stage": config.stage,
            "school_day": config.school_day,
            "start_time": config.start_time,
            "sessions_per_day": config.sessions_per_day,
            "session_duration_minutes": config.session_duration_minutes,
            "break_after_period": config.break_after_period,
            "break_duration_minutes": config.break_duration_minutes,
        }

        con = self._connect()
        try:
            for key, value in data.items():
                con.execute(
                    "INSERT OR REPLACE INTO center_config(key, value) VALUES(?, ?)",
                    (key, str(value)),
                )
            con.commit()
        finally:
            con.close()

    def get_config(self) -> CenterConfig:
        con = self._connect()
        try:
            rows = con.execute("SELECT key, value FROM center_config").fetchall()
            values = {row["key"]: row["value"] for row in rows}
        finally:
            con.close()

        if not values:
            return CenterConfig()

        return CenterConfig(
            center_name=values.get("center_name", "CEIP Tierra de Pinares"),
            center_code=values.get("center_code", ""),
            locality=values.get("locality", "Mojados"),
            province=values.get("province", "Valladolid"),
            school_year=values.get("school_year", "2026/2027"),
            center_type=values.get("center_type", "CEIP"),
            stage=values.get("stage", "Primaria"),
            school_day=values.get("school_day", "Continua"),
            start_time=values.get("start_time", "09:00"),
            sessions_per_day=int(values.get("sessions_per_day", 6)),
            session_duration_minutes=int(values.get("session_duration_minutes", 45)),
            break_after_period=int(values.get("break_after_period", 3)),
            break_duration_minutes=int(values.get("break_duration_minutes", 30)),
        )
