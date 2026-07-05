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

from pini_desktop.services.course_service import Course, CourseService
from pini_desktop.ui.dialogs.course_dialog import CourseDialog


class CoursesView(QWidget):
    HEADERS = ["ID", "Código", "Etapa", "Nivel", "Grupo", "Alumnado"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = CourseService()

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_selected_course)

        add_button = QPushButton("Añadir curso")
        add_button.clicked.connect(self.add_course)

        edit_button = QPushButton("Editar")
        edit_button.clicked.connect(self.edit_selected_course)

        delete_button = QPushButton("Eliminar")
        delete_button.clicked.connect(self.delete_selected_course)

        refresh_button = QPushButton("Actualizar")
        refresh_button.clicked.connect(self.load_courses)

        buttons = QHBoxLayout()
        buttons.addWidget(add_button)
        buttons.addWidget(edit_button)
        buttons.addWidget(delete_button)
        buttons.addStretch()
        buttons.addWidget(refresh_button)

        layout = QVBoxLayout(self)
        layout.addLayout(buttons)
        layout.addWidget(self.table)

        self.load_courses()

    def load_courses(self) -> None:
        courses = self.service.list_courses()
        self.table.setRowCount(len(courses))

        for row_index, course in enumerate(courses):
            values = [
                course.id,
                course.code,
                course.stage,
                course.level,
                course.group_name,
                course.students,
            ]
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                if column_index == 0:
                    item.setData(Qt.UserRole, course)
                self.table.setItem(row_index, column_index, item)

        self.table.resizeColumnsToContents()

    def add_course(self) -> None:
        dialog = CourseDialog(self)
        if dialog.exec():
            try:
                self.service.create_course(dialog.get_course())
                self.load_courses()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Código duplicado", "Ya existe un curso con ese código.")

    def edit_selected_course(self) -> None:
        course = self._selected_course()
        if course is None:
            QMessageBox.information(self, "Selecciona curso", "Selecciona un curso para editar.")
            return

        dialog = CourseDialog(self, course)
        if dialog.exec():
            try:
                self.service.update_course(dialog.get_course())
                self.load_courses()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Código duplicado", "Ya existe un curso con ese código.")

    def delete_selected_course(self) -> None:
        course = self._selected_course()
        if course is None:
            QMessageBox.information(self, "Selecciona curso", "Selecciona un curso para eliminar.")
            return

        response = QMessageBox.question(
            self,
            "Eliminar curso",
            f"¿Eliminar el curso {course.code}?",
        )
        if response == QMessageBox.Yes:
            self.service.delete_course(course.id)
            self.load_courses()

    def _selected_course(self) -> Course | None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return None
        row = selected[0].row()
        item = self.table.item(row, 0)
        return item.data(Qt.UserRole)
