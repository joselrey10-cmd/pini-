import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database


@dataclass(frozen=True)
class TimetablePeriod:
    id: int | None
    day: int
    period: int
    start_time: str
    end_time: str
    is_break_after: bool = False
    is_after_break: bool = False


@dataclass(frozen=True)
class TimetableSettings:
    working_days: int = 5
    sessions_per_day: int = 6
    session_duration_minutes: int = 45
    break_after_period: int = 3
    break_duration_minutes: int = 30
    start_time: str = "09:00"


class TimetableService:
    DAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        initialise_database()

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def get_settings(self) -> TimetableSettings:
        connection = self._connect()
        try:
            rows = connection.execute("SELECT key, value FROM timetable_settings").fetchall()
            values = {row["key"]: row["value"] for row in rows}
            if not values:
                return TimetableSettings()
            return TimetableSettings(
                working_days=int(values.get("working_days", 5)),
                sessions_per_day=int(values.get("sessions_per_day", 6)),
                session_duration_minutes=int(values.get("session_duration_minutes", 45)),
                break_after_period=int(values.get("break_after_period", 3)),
                break_duration_minutes=int(values.get("break_duration_minutes", 30)),
                start_time=values.get("start_time", "09:00"),
            )
        finally:
            connection.close()

    def save_settings(self, settings: TimetableSettings) -> None:
        connection = self._connect()
        try:
            data = {
                "working_days": settings.working_days,
                "sessions_per_day": settings.sessions_per_day,
                "session_duration_minutes": settings.session_duration_minutes,
                "break_after_period": settings.break_after_period,
                "break_duration_minutes": settings.break_duration_minutes,
                "start_time": settings.start_time,
            }
            for key, value in data.items():
                connection.execute(
                    "INSERT OR REPLACE INTO timetable_settings(key, value) VALUES(?, ?)",
                    (key, str(value)),
                )
            connection.commit()
        finally:
            connection.close()

    def generate_periods(self, settings: TimetableSettings | None = None) -> list[TimetablePeriod]:
        settings = settings or self.get_settings()
        periods = []
        base = datetime.strptime(settings.start_time, "%H:%M")

        for day in range(1, settings.working_days + 1):
            current = base
            for period in range(1, settings.sessions_per_day + 1):
                start = current
                end = start + timedelta(minutes=settings.session_duration_minutes)
                periods.append(
                    TimetablePeriod(
                        id=None,
                        day=day,
                        period=period,
                        start_time=start.strftime("%H:%M"),
                        end_time=end.strftime("%H:%M"),
                        is_break_after=period == settings.break_after_period,
                        is_after_break=period > settings.break_after_period,
                    )
                )
                current = end
                if period == settings.break_after_period:
                    current += timedelta(minutes=settings.break_duration_minutes)

        return periods

    def save_generated_periods(self, settings: TimetableSettings | None = None) -> None:
        periods = self.generate_periods(settings)
        connection = self._connect()
        try:
            connection.execute("DELETE FROM timetable_periods")
            for period in periods:
                connection.execute(
                    '''
                    INSERT INTO timetable_periods(day, period, start_time, end_time, is_break_after, is_after_break)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        period.day,
                        period.period,
                        period.start_time,
                        period.end_time,
                        int(period.is_break_after),
                        int(period.is_after_break),
                    ),
                )
            connection.commit()
        finally:
            connection.close()

    def list_periods(self) -> list[TimetablePeriod]:
        connection = self._connect()
        try:
            rows = connection.execute(
                '''
                SELECT id, day, period, start_time, end_time, is_break_after, is_after_break
                FROM timetable_periods
                ORDER BY day, period
                '''
            ).fetchall()
            return [
                TimetablePeriod(
                    id=int(row["id"]),
                    day=int(row["day"]),
                    period=int(row["period"]),
                    start_time=row["start_time"],
                    end_time=row["end_time"],
                    is_break_after=bool(row["is_break_after"]),
                    is_after_break=bool(row["is_after_break"]),
                )
                for row in rows
            ]
        finally:
            connection.close()
