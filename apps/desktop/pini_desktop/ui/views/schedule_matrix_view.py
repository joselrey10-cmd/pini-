from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMenu,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from pini_desktop.services.editor.editor_service import EditorService
from pini_desktop.services.schedule_view_service import ScheduleViewService


class ScheduleMatrixView(QWidget):
    DAY_NAMES = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    SESSION_ID_ROLE = Qt.UserRole
    DAY_ROLE = Qt.UserRole + 1
    PERIOD_ROLE = Qt.UserRole + 2

    def __init__(self, mode: str, parent=None):
        super().__init__(parent)
        if mode not in {"course", "teacher"}:
            raise ValueError("mode debe ser 'course' o 'teacher'")
        self.mode = mode
        self.service = ScheduleViewService()
        self.editor_service = EditorService()
        self.marked_session_id: int | None = None
        self.marked_session_label = ""

        self.selector = QComboBox()
        self.selector.currentIndexChanged.connect(self.load_matrix)

        refresh_button = QPushButton("Actualizar")
        refresh_button.clicked.connect(self.reload_entities)

        undo_button = QPushButton("Deshacer")
        undo_button.clicked.connect(self.undo_last_action)

        redo_button = QPushButton("Rehacer")
        redo_button.clicked.connect(self.redo_last_action)

        self.status_label = QLabel("Editor: selecciona una sesión con botón derecho.")
        self.status_label.setWordWrap(True)

        top = QHBoxLayout()
        top.addWidget(QLabel("Curso:" if mode == "course" else "Profesor/a:"))
        top.addWidget(self.selector)
        top.addStretch()
        top.addWidget(refresh_button)
        top.addWidget(undo_button)
        top.addWidget(redo_button)

        self.table = QTableWidget()
        self.table.setRowCount(6)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(self.DAY_NAMES)
        self.table.setVerticalHeaderLabels([f"P{i}" for i in range(1, 7)])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_context_menu)

        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addWidget(self.status_label)
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

        for day in range(1, 6):
            for period in range(1, 7):
                self._set_empty_cell(day, period)

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
                    continue

                if self.mode == "course":
                    text = f"{cell.subject_name}\n{cell.teacher_name}\n{cell.room_name}".strip()
                else:
                    text = f"{cell.course_code}\n{cell.subject_name}\n{cell.room_name}".strip()

                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                item.setData(self.SESSION_ID_ROLE, cell.id)
                item.setData(self.DAY_ROLE, day)
                item.setData(self.PERIOD_ROLE, period)
                self.table.setItem(period - 1, day - 1, item)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def _set_empty_cell(self, day: int, period: int) -> None:
        item = QTableWidgetItem("")
        item.setTextAlignment(Qt.AlignCenter)
        item.setData(self.SESSION_ID_ROLE, None)
        item.setData(self.DAY_ROLE, day)
        item.setData(self.PERIOD_ROLE, period)
        self.table.setItem(period - 1, day - 1, item)

    def open_context_menu(self, position) -> None:
        item = self.table.itemAt(position)
        if item is None:
            return

        session_id = item.data(self.SESSION_ID_ROLE)
        day = item.data(self.DAY_ROLE)
        period = item.data(self.PERIOD_ROLE)

        menu = QMenu(self)

        if session_id is not None:
            mark_action = menu.addAction("Marcar esta sesión para mover/intercambiar")
            mark_action.triggered.connect(lambda: self.mark_session(session_id, item.text()))

        if self.marked_session_id is not None:
            if session_id is None:
                move_action = menu.addAction("Mover sesión marcada aquí")
                move_action.triggered.connect(lambda: self.move_marked_session(day, period))
            elif session_id != self.marked_session_id:
                swap_action = menu.addAction("Intercambiar con la sesión marcada")
                swap_action.triggered.connect(lambda: self.swap_marked_session(session_id))

            clear_action = menu.addAction("Cancelar selección marcada")
            clear_action.triggered.connect(self.clear_marked_session)

        menu.exec(self.table.viewport().mapToGlobal(position))

    def mark_session(self, session_id: int, label: str) -> None:
        self.marked_session_id = int(session_id)
        self.marked_session_label = label.replace("\n", " / ")
        self.status_label.setText(f"Sesión marcada: {self.marked_session_label}")

    def clear_marked_session(self) -> None:
        self.marked_session_id = None
        self.marked_session_label = ""
        self.status_label.setText("Editor: selección cancelada.")

    def move_marked_session(self, day: int, period: int) -> None:
        if self.marked_session_id is None:
            return

        result = self.editor_service.move_session(self.marked_session_id, day, period)
        self._show_result(result)
        if result.success:
            self.clear_marked_session()
            self.load_matrix()

    def swap_marked_session(self, other_session_id: int) -> None:
        if self.marked_session_id is None:
            return

        result = self.editor_service.swap_sessions(self.marked_session_id, int(other_session_id))
        self._show_result(result)
        if result.success:
            self.clear_marked_session()
            self.load_matrix()

    def undo_last_action(self) -> None:
        result = self.editor_service.undo()
        self._show_result(result)
        if result.success:
            self.load_matrix()

    def redo_last_action(self) -> None:
        result = self.editor_service.redo()
        self._show_result(result)
        if result.success:
            self.load_matrix()

    def _show_result(self, result) -> None:
        details = []
        if result.messages:
            details.extend(result.messages)
        if result.warnings:
            details.append("")
            details.append("Avisos:")
            details.extend(result.warnings)

        text = "\n".join(details) if details else ("Operación correcta." if result.success else "Operación no realizada.")
        self.status_label.setText(text.replace("\n", " · "))

        if result.success:
            QMessageBox.information(self, "Editor de horario", text)
        else:
            QMessageBox.warning(self, "Editor de horario", text)


class CourseScheduleView(ScheduleMatrixView):
    def __init__(self, parent=None):
        super().__init__("course", parent)


class TeacherScheduleView(ScheduleMatrixView):
    def __init__(self, parent=None):
        super().__init__("teacher", parent)
