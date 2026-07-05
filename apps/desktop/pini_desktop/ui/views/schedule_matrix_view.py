from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from pini_desktop.services.schedule_view_service import ScheduleViewService


class ScheduleMatrixView(QWidget):
    DAY_NAMES = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    def __init__(self, mode: str, parent=None):
        super().__init__(parent)
        if mode not in {"course", "teacher"}:
            raise ValueError("mode debe ser 'course' o 'teacher'")
        self.mode = mode
        self.service = ScheduleViewService()

        self.selector = QComboBox()
        self.selector.currentIndexChanged.connect(self.load_matrix)

        refresh_button = QPushButton("Actualizar")
        refresh_button.clicked.connect(self.reload_entities)

        top = QHBoxLayout()
        top.addWidget(QLabel("Curso:" if mode == "course" else "Profesor/a:"))
        top.addWidget(self.selector)
        top.addStretch()
        top.addWidget(refresh_button)

        self.table = QTableWidget()
        self.table.setRowCount(6)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(self.DAY_NAMES)
        self.table.setVerticalHeaderLabels([f"P{i}" for i in range(1, 7)])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addWidget(self.table)

        self.reload_entities()

    def reload_entities(self) -> None:
        current = self.selector.currentData()
        self.selector.blockSignals(True)
        self.selector.clear()

        if self.mode == "course":
            items = self.service.list_courses()
        else:
            items = self.service.list_teachers()

        for entity_id, label in items:
            self.selector.addItem(label, entity_id)

        if current is not None:
            for index in range(self.selector.count()):
                if self.selector.itemData(index) == current:
                    self.selector.setCurrentIndex(index)
                    break

        self.selector.blockSignals(False)
        self.load_matrix()

    def load_matrix(self) -> None:
        entity_id = self.selector.currentData()
        self.table.clearContents()

        if entity_id is None:
            return

        if self.mode == "course":
            matrix = self.service.course_matrix(entity_id)
        else:
            matrix = self.service.teacher_matrix(entity_id)

        for day in range(1, 6):
            for period in range(1, 7):
                cell = matrix.get((day, period))
                if cell is None:
                    text = ""
                elif self.mode == "course":
                    text = f"{cell.subject_name}\n{cell.teacher_name}\n{cell.room_name}".strip()
                else:
                    text = f"{cell.course_code}\n{cell.subject_name}\n{cell.room_name}".strip()

                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(period - 1, day - 1, item)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()


class CourseScheduleView(ScheduleMatrixView):
    def __init__(self, parent=None):
        super().__init__("course", parent)


class TeacherScheduleView(ScheduleMatrixView):
    def __init__(self, parent=None):
        super().__init__("teacher", parent)
