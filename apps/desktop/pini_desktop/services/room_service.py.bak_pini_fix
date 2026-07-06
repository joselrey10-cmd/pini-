import sqlite3
from dataclasses import dataclass

from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database


@dataclass(frozen=True)
class Room:
    id: int | None
    code: str
    name: str
    room_type: str
    capacity: int = 25
    building: str = ""
    resources: str = ""
    available: bool = True


class RoomService:
    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        initialise_database()

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def list_rooms(self) -> list[Room]:
        connection = self._connect()
        try:
            rows = connection.execute(
                '''
                SELECT id, code, name, room_type, capacity, building, resources, available
                FROM rooms
                ORDER BY room_type, code
                '''
            ).fetchall()
            return [self._row_to_room(row) for row in rows]
        finally:
            connection.close()

    def create_room(self, room: Room) -> int:
        connection = self._connect()
        try:
            cursor = connection.execute(
                '''
                INSERT INTO rooms(code, name, room_type, capacity, building, resources, available)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    room.code.strip().upper(),
                    room.name.strip(),
                    room.room_type.strip(),
                    int(room.capacity),
                    room.building.strip(),
                    room.resources.strip(),
                    int(room.available),
                ),
            )
            connection.commit()
            return int(cursor.lastrowid)
        finally:
            connection.close()

    def update_room(self, room: Room) -> None:
        if room.id is None:
            raise ValueError("No se puede actualizar un aula sin id.")

        connection = self._connect()
        try:
            connection.execute(
                '''
                UPDATE rooms
                SET code=?, name=?, room_type=?, capacity=?, building=?, resources=?, available=?
                WHERE id=?
                ''',
                (
                    room.code.strip().upper(),
                    room.name.strip(),
                    room.room_type.strip(),
                    int(room.capacity),
                    room.building.strip(),
                    room.resources.strip(),
                    int(room.available),
                    room.id,
                ),
            )
            connection.commit()
        finally:
            connection.close()

    def delete_room(self, room_id: int) -> None:
        connection = self._connect()
        try:
            connection.execute("DELETE FROM rooms WHERE id=?", (room_id,))
            connection.commit()
        finally:
            connection.close()

    def seed_default_rooms(self) -> None:
        if self.list_rooms():
            return
        defaults = [
            Room(None, "A1", "Aula 1", "Ordinaria", 25, "Principal", "", True),
            Room(None, "A2", "Aula 2", "Ordinaria", 25, "Principal", "", True),
            Room(None, "A3", "Aula 3", "Ordinaria", 25, "Principal", "", True),
            Room(None, "GIM", "Gimnasio", "Gimnasio", 50, "Principal", "Material EF", True),
            Room(None, "MUS", "Aula de Música", "Música", 25, "Principal", "Instrumentos", True),
            Room(None, "PT", "Aula PT", "PT", 8, "Principal", "", True),
            Room(None, "AL", "Aula AL", "AL", 6, "Principal", "", True),
            Room(None, "BIB", "Biblioteca", "Biblioteca", 30, "Principal", "Libros", True),
            Room(None, "TIC", "Aula TIC", "Informática", 25, "Principal", "Ordenadores", True),
        ]
        for room in defaults:
            self.create_room(room)

    def _row_to_room(self, row) -> Room:
        return Room(
            id=int(row["id"]),
            code=row["code"],
            name=row["name"],
            room_type=row["room_type"],
            capacity=int(row["capacity"]),
            building=row["building"] or "",
            resources=row["resources"] or "",
            available=bool(row["available"]),
        )
