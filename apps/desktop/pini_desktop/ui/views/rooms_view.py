import sqlite3

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from pini_desktop.services.room_service import Room, RoomService
from pini_desktop.ui.dialogs.room_dialog import RoomDialog


class RoomsView(QWidget):
    HEADERS = ["ID", "Código", "Nombre", "Tipo", "Capacidad", "Edificio", "Recursos", "Disponible"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = RoomService()

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_selected_room)

        add_button = QPushButton("Añadir aula")
        add_button.clicked.connect(self.add_room)

        edit_button = QPushButton("Editar")
        edit_button.clicked.connect(self.edit_selected_room)

        delete_button = QPushButton("Eliminar")
        delete_button.clicked.connect(self.delete_selected_room)

        seed_button = QPushButton("Cargar aulas base")
        seed_button.clicked.connect(self.seed_rooms)

        refresh_button = QPushButton("Actualizar")
        refresh_button.clicked.connect(self.load_rooms)

        buttons = QHBoxLayout()
        buttons.addWidget(add_button)
        buttons.addWidget(edit_button)
        buttons.addWidget(delete_button)
        buttons.addWidget(seed_button)
        buttons.addStretch()
        buttons.addWidget(refresh_button)

        layout = QVBoxLayout(self)
        layout.addLayout(buttons)
        layout.addWidget(self.table)

        self.load_rooms()

    def load_rooms(self) -> None:
        rooms = self.service.list_rooms()
        self.table.setRowCount(len(rooms))

        for row_index, room in enumerate(rooms):
            values = [
                room.id,
                room.code,
                room.name,
                room.room_type,
                room.capacity,
                room.building,
                room.resources,
                "Sí" if room.available else "No",
            ]
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                if column_index == 0:
                    item.setData(Qt.UserRole, room)
                self.table.setItem(row_index, column_index, item)

        self.table.resizeColumnsToContents()

    def add_room(self) -> None:
        dialog = RoomDialog(self)
        if dialog.exec():
            try:
                self.service.create_room(dialog.get_room())
                self.load_rooms()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Código duplicado", "Ya existe un aula con ese código.")

    def edit_selected_room(self) -> None:
        room = self._selected_room()
        if room is None:
            QMessageBox.information(self, "Selecciona aula", "Selecciona un aula para editar.")
            return

        dialog = RoomDialog(self, room)
        if dialog.exec():
            try:
                self.service.update_room(dialog.get_room())
                self.load_rooms()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Código duplicado", "Ya existe un aula con ese código.")

    def delete_selected_room(self) -> None:
        room = self._selected_room()
        if room is None:
            QMessageBox.information(self, "Selecciona aula", "Selecciona un aula para eliminar.")
            return

        response = QMessageBox.question(
            self,
            "Eliminar aula",
            f"¿Eliminar el aula {room.name}?",
        )
        if response == QMessageBox.Yes:
            self.service.delete_room(room.id)
            self.load_rooms()

    def seed_rooms(self) -> None:
        self.service.seed_default_rooms()
        self.load_rooms()

    def _selected_room(self) -> Room | None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return None
        row = selected[0].row()
        item = self.table.item(row, 0)
        return item.data(Qt.UserRole)
