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

from pini_desktop.services.course_subject_service import CourseSubject, CourseSubjectService
from pini_desktop.ui.dialogs.course_subject_dialog import CourseSubjectDialog


class CourseSubjectsView(QWidget):
    HEADERS = ["ID", "Curso", "Materia", "Sesiones", "Profesor preferente", "Aula", "Notas"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = CourseSubjectService()

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_selected_assignment)

        add_button = QPushButton("Añadir asignación")
        add_button.clicked.connect(self.add_assignment)

        edit_button = QPushButton("Editar")
        edit_button.clicked.connect(self.edit_selected_assignment)

        delete_button = QPushButton("Eliminar")
        delete_button.clicked.connect(self.delete_selected_assignment)

        refresh_button = QPushButton("Actualizar")
        refresh_button.clicked.connect(self.load_assignments)

        buttons = QHBoxLayout()
        buttons.addWidget(add_button)
        buttons.addWidget(edit_button)
        buttons.addWidget(delete_button)
        buttons.addStretch()
        buttons.addWidget(refresh_button)

        layout = QVBoxLayout(self)
        layout.addLayout(buttons)
        layout.addWidget(self.table)

        self.load_assignments()

    def load_assignments(self) -> None:
        assignments = self.service.list_assignments()
        self.table.setRowCount(len(assignments))

        for row_index, assignment in enumerate(assignments):
            values = [
                assignment.id,
                assignment.course_code,
                assignment.subject_name,
                assignment.weekly_sessions,
                assignment.teacher_name,
                assignment.required_room_type,
                assignment.notes,
            ]
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                if column_index == 0:
                    item.setData(Qt.UserRole, assignment)
                self.table.setItem(row_index, column_index, item)

        self.table.resizeColumnsToContents()

    def add_assignment(self) -> None:
        dialog = CourseSubjectDialog(self)
        if dialog.exec():
            try:
                self.service.create_assignment(dialog.get_assignment())
                self.load_assignments()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Asignación duplicada", "Este curso ya tiene asignada esa materia.")

    def edit_selected_assignment(self) -> None:
        assignment = self._selected_assignment()
        if assignment is None:
            QMessageBox.information(self, "Selecciona asignación", "Selecciona una asignación para editar.")
            return

        dialog = CourseSubjectDialog(self, assignment)
        if dialog.exec():
            try:
                self.service.update_assignment(dialog.get_assignment())
                self.load_assignments()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Asignación duplicada", "Este curso ya tiene asignada esa materia.")

    def delete_selected_assignment(self) -> None:
        assignment = self._selected_assignment()
        if assignment is None:
            QMessageBox.information(self, "Selecciona asignación", "Selecciona una asignación para eliminar.")
            return

        response = QMessageBox.question(
            self,
            "Eliminar asignación",
            f"¿Eliminar {assignment.subject_name} de {assignment.course_code}?",
        )
        if response == QMessageBox.Yes:
            self.service.delete_assignment(assignment.id)
            self.load_assignments()

    def _selected_assignment(self) -> CourseSubject | None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return None
        row = selected[0].row()
        item = self.table.item(row, 0)
        return item.data(Qt.UserRole)
