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

from pini_desktop.services.subject_service import Subject, SubjectService
from pini_desktop.ui.dialogs.subject_dialog import SubjectDialog


class SubjectsView(QWidget):
    HEADERS = [
        "ID", "Código", "Nombre", "Sesiones", "Especialidad",
        "Aula", "Máx. consecutivas", "Doble"
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = SubjectService()

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_selected_subject)

        add_button = QPushButton("Añadir materia")
        add_button.clicked.connect(self.add_subject)

        edit_button = QPushButton("Editar")
        edit_button.clicked.connect(self.edit_selected_subject)

        delete_button = QPushButton("Eliminar")
        delete_button.clicked.connect(self.delete_selected_subject)

        seed_button = QPushButton("Cargar materias base")
        seed_button.clicked.connect(self.seed_subjects)

        refresh_button = QPushButton("Actualizar")
        refresh_button.clicked.connect(self.load_subjects)

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

        self.load_subjects()

    def load_subjects(self) -> None:
        subjects = self.service.list_subjects()
        self.table.setRowCount(len(subjects))

        for row_index, subject in enumerate(subjects):
            values = [
                subject.id,
                subject.code,
                subject.name,
                subject.weekly_sessions,
                subject.required_speciality,
                subject.room_type,
                subject.max_consecutive,
                "Sí" if subject.allows_double_session else "No",
            ]
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                if column_index == 0:
                    item.setData(Qt.UserRole, subject)
                self.table.setItem(row_index, column_index, item)

        self.table.resizeColumnsToContents()

    def add_subject(self) -> None:
        dialog = SubjectDialog(self)
        if dialog.exec():
            try:
                self.service.create_subject(dialog.get_subject())
                self.load_subjects()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Código duplicado", "Ya existe una materia con ese código.")

    def edit_selected_subject(self) -> None:
        subject = self._selected_subject()
        if subject is None:
            QMessageBox.information(self, "Selecciona materia", "Selecciona una materia para editar.")
            return

        dialog = SubjectDialog(self, subject)
        if dialog.exec():
            try:
                self.service.update_subject(dialog.get_subject())
                self.load_subjects()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Código duplicado", "Ya existe una materia con ese código.")

    def delete_selected_subject(self) -> None:
        subject = self._selected_subject()
        if subject is None:
            QMessageBox.information(self, "Selecciona materia", "Selecciona una materia para eliminar.")
            return

        response = QMessageBox.question(
            self,
            "Eliminar materia",
            f"¿Eliminar la materia {subject.name}?",
        )
        if response == QMessageBox.Yes:
            self.service.delete_subject(subject.id)
            self.load_subjects()

    def seed_subjects(self) -> None:
        self.service.seed_default_subjects()
        self.load_subjects()

    def _selected_subject(self) -> Subject | None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return None
        row = selected[0].row()
        item = self.table.item(row, 0)
        return item.data(Qt.UserRole)
