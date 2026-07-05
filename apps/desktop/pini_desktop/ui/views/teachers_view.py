import sqlite3
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from pini_desktop.services.teacher_service import Teacher, TeacherService
from pini_desktop.ui.dialogs.teacher_dialog import TeacherDialog

class TeachersView(QWidget):
    HEADERS = ["ID", "Código", "Nombre", "Apellidos", "Especialidad", "Horas", "Máx. diario"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = TeacherService()
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_selected_teacher)

        add_button = QPushButton("Añadir profesor")
        add_button.clicked.connect(self.add_teacher)
        edit_button = QPushButton("Editar")
        edit_button.clicked.connect(self.edit_selected_teacher)
        delete_button = QPushButton("Eliminar")
        delete_button.clicked.connect(self.delete_selected_teacher)
        refresh_button = QPushButton("Actualizar")
        refresh_button.clicked.connect(self.load_teachers)

        buttons = QHBoxLayout()
        buttons.addWidget(add_button)
        buttons.addWidget(edit_button)
        buttons.addWidget(delete_button)
        buttons.addStretch()
        buttons.addWidget(refresh_button)

        layout = QVBoxLayout(self)
        layout.addLayout(buttons)
        layout.addWidget(self.table)
        self.load_teachers()

    def load_teachers(self) -> None:
        teachers = self.service.list_teachers()
        self.table.setRowCount(len(teachers))
        for row_index, teacher in enumerate(teachers):
            values = [teacher.id, teacher.code, teacher.name, teacher.surname, teacher.speciality, teacher.weekly_hours, teacher.max_daily_sessions]
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                if column_index == 0:
                    item.setData(Qt.UserRole, teacher)
                self.table.setItem(row_index, column_index, item)
        self.table.resizeColumnsToContents()

    def add_teacher(self) -> None:
        dialog = TeacherDialog(self)
        if dialog.exec():
            try:
                self.service.create_teacher(dialog.get_teacher())
                self.load_teachers()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Código duplicado", "Ya existe un profesor con ese código.")

    def edit_selected_teacher(self) -> None:
        teacher = self._selected_teacher()
        if teacher is None:
            QMessageBox.information(self, "Selecciona profesor", "Selecciona un profesor para editar.")
            return
        dialog = TeacherDialog(self, teacher)
        if dialog.exec():
            try:
                self.service.update_teacher(dialog.get_teacher())
                self.load_teachers()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Código duplicado", "Ya existe un profesor con ese código.")

    def delete_selected_teacher(self) -> None:
        teacher = self._selected_teacher()
        if teacher is None:
            QMessageBox.information(self, "Selecciona profesor", "Selecciona un profesor para eliminar.")
            return
        response = QMessageBox.question(self, "Eliminar profesor", f"¿Eliminar a {teacher.full_name}?")
        if response == QMessageBox.Yes:
            self.service.delete_teacher(teacher.id)
            self.load_teachers()

    def _selected_teacher(self) -> Teacher | None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return None
        item = self.table.item(selected[0].row(), 0)
        return item.data(Qt.UserRole)
