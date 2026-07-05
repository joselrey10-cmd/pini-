import sqlite3
from dataclasses import dataclass
from enum import Enum

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database


class AvailabilityStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    PREFERRED = "PREFERRED"
    AVOID = "AVOID"
    FORBIDDEN = "FORBIDDEN"


@dataclass(frozen=True)
class AvailabilityCell:
    teacher_id: int
    day: int
    period: int
    status: AvailabilityStatus


class AvailabilityService:
    DAYS = [1, 2, 3, 4, 5]
    PERIODS = [1, 2, 3, 4, 5, 6]

    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        initialise_database()

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialise_teacher(self, teacher_id: int) -> None:
        connection = self._connect()
        try:
            for day in self.DAYS:
                for period in self.PERIODS:
                    connection.execute(
                        '''
                        INSERT OR IGNORE INTO teacher_availability(teacher_id, day, period, status)
                        VALUES (?, ?, ?, ?)
                        ''',
                        (teacher_id, day, period, AvailabilityStatus.AVAILABLE.value),
                    )
            connection.commit()
        finally:
            connection.close()

    def get_matrix(self, teacher_id: int) -> dict[tuple[int, int], AvailabilityStatus]:
        self.initialise_teacher(teacher_id)
        connection = self._connect()
        try:
            rows = connection.execute(
                '''
                SELECT day, period, status
                FROM teacher_availability
                WHERE teacher_id=?
                ORDER BY day, period
                ''',
                (teacher_id,),
            ).fetchall()
            return {
                (int(row["day"]), int(row["period"])): AvailabilityStatus(row["status"])
                for row in rows
            }
        finally:
            connection.close()

    def set_status(self, teacher_id: int, day: int, period: int, status: AvailabilityStatus) -> None:
        connection = self._connect()
        try:
            connection.execute(
                '''
                INSERT OR REPLACE INTO teacher_availability(teacher_id, day, period, status)
                VALUES (?, ?, ?, ?)
                ''',
                (teacher_id, int(day), int(period), status.value),
            )
            connection.commit()
        finally:
            connection.close()

    def set_matrix(self, teacher_id: int, matrix: dict[tuple[int, int], AvailabilityStatus]) -> None:
        connection = self._connect()
        try:
            for (day, period), status in matrix.items():
                connection.execute(
                    '''
                    INSERT OR REPLACE INTO teacher_availability(teacher_id, day, period, status)
                    VALUES (?, ?, ?, ?)
                    ''',
                    (teacher_id, int(day), int(period), status.value),
                )
            connection.commit()
        finally:
            connection.close()
