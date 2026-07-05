from pathlib import Path

from pini_desktop.services.room_service import Room, RoomService


def test_room_crud(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    service = RoomService(database_path=db)

    room_id = service.create_room(
        Room(
            id=None,
            code="GIM",
            name="Gimnasio",
            room_type="Gimnasio",
            capacity=50,
            building="Principal",
            resources="Material EF",
            available=True,
        )
    )

    rooms = service.list_rooms()
    assert len(rooms) == 1
    assert rooms[0].id == room_id
    assert rooms[0].code == "GIM"

    service.update_room(
        Room(
            id=room_id,
            code="GIM",
            name="Gimnasio principal",
            room_type="Gimnasio",
            capacity=55,
            building="Principal",
            resources="Material EF",
            available=True,
        )
    )

    assert service.list_rooms()[0].capacity == 55

    service.delete_room(room_id)
    assert service.list_rooms() == []


def test_seed_default_rooms(tmp_path: Path):
    db = tmp_path / "test_pini.db"
    service = RoomService(database_path=db)
    service.seed_default_rooms()

    codes = {room.code for room in service.list_rooms()}
    assert "GIM" in codes
    assert "PT" in codes
    assert "AL" in codes
