from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from pini_desktop.services.room_service import Room


class RoomDialog(QDialog):
    def __init__(self, parent=None, room: Room | None = None):
        super().__init__(parent)
        self.setWindowTitle("Aula")
        self.room = room

        self.code_input = QLineEdit()
        self.name_input = QLineEdit()

        self.room_type_input = QComboBox()
        self.room_type_input.addItems([
            "Ordinaria",
            "Gimnasio",
            "Música",
            "PT",
            "AL",
            "Biblioteca",
            "Informática",
            "Apoyo",
            "Otro",
        ])

        self.capacity_input = QSpinBox()
        self.capacity_input.setRange(1, 200)
        self.capacity_input.setValue(25)

        self.building_input = QLineEdit()
        self.resources_input = QLineEdit()
        self.available_input = QCheckBox("Disponible")
        self.available_input.setChecked(True)

        if room is not None:
            self.code_input.setText(room.code)
            self.name_input.setText(room.name)
            index = self.room_type_input.findText(room.room_type)
            if index >= 0:
                self.room_type_input.setCurrentIndex(index)
            self.capacity_input.setValue(room.capacity)
            self.building_input.setText(room.building)
            self.resources_input.setText(room.resources)
            self.available_input.setChecked(room.available)

        form = QFormLayout()
        form.addRow("Código", self.code_input)
        form.addRow("Nombre", self.name_input)
        form.addRow("Tipo", self.room_type_input)
        form.addRow("Capacidad", self.capacity_input)
        form.addRow("Edificio", self.building_input)
        form.addRow("Recursos", self.resources_input)
        form.addRow("", self.available_input)

        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self._accept_if_valid)

        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)

        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addLayout(buttons)

    def get_room(self) -> Room:
        return Room(
            id=self.room.id if self.room else None,
            code=self.code_input.text().strip().upper(),
            name=self.name_input.text().strip(),
            room_type=self.room_type_input.currentText().strip(),
            capacity=self.capacity_input.value(),
            building=self.building_input.text().strip(),
            resources=self.resources_input.text().strip(),
            available=self.available_input.isChecked(),
        )

    def _accept_if_valid(self) -> None:
        room = self.get_room()
        if not room.code or not room.name:
            QMessageBox.warning(self, "Datos incompletos", "Rellena código y nombre.")
            return
        self.accept()
