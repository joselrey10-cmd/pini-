from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMenu,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from pini_desktop.services.editor.editor_service import EditorService
from pini_desktop.services.editor.validation.live_validation import LiveMoveValidator
from pini_desktop.services.schedule_view_service import ScheduleViewService
from pini_desktop.ui.views.editor_history_panel import EditorHistoryPanel
from pini_desktop.ui.views.editor_impact_panel import EditorImpactPanel
from pini_desktop.ui.views.local_optimization_panel import LocalOptimizationPanel
from pini_desktop.ui.views.schedule_dragdrop_table import ScheduleDragDropTable
from pini_desktop.ui.views.schedule_versions_panel import ScheduleVersionsPanel


class ScheduleMatrixView(QWidget):
    DAY_NAMES = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    SESSION_ID_ROLE = Qt.UserRole
    DAY_ROLE = Qt.UserRole + 1
    PERIOD_ROLE = Qt.UserRole + 2

    COLOR_DEFAULT = QColor(255, 255, 255)
    COLOR_VALID = QColor(210, 245, 220)
    COLOR_SWAP = QColor(255, 240, 190)
    COLOR_SAME = QColor(230, 230, 230)

    def __init__(self, mode: str, parent=None):
        super().__init__(parent)
        if mode not in {"course", "teacher"}:
            raise ValueError("mode debe ser 'course' o 'teacher'")
        self.mode = mode
        self.service = ScheduleViewService()
        self.editor_service = EditorService()
        self.live_validator = LiveMoveValidator()
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

        self.status_label = QLabel("Editor: arrastra una sesión o usa botón derecho.")
        self.status_label.setWordWrap(True)

        top = QHBoxLayout()
        top.addWidget(QLabel("Curso:" if mode == "course" else "Profesor/a:"))
        top.addWidget(self.selector)
        top.addStretch()
        top.addWidget(refresh_button)
        top.addWidget(undo_button)
        top.addWidget(redo_button)

        self.table = ScheduleDragDropTable()
        self.table.setRowCount(6)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(self.DAY_NAMES)
        self.table.setVerticalHeaderLabels([f"P{i}" for i in range(1, 7)])
        self.table.setEditTriggers(ScheduleDragDropTable.NoEditTriggers)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_context_menu)
        self.table.sessionMoved.connect(self.move_session_by_drag)
        self.table.sessionsSwapped.connect(self.swap_sessions_by_drag)
        self.table.dragPreviewRequested.connect(self.preview_drag_target)
        self.table.dragPreviewCleared.connect(self.clear_live_preview)

        self.impact_panel = EditorImpactPanel()
        self.history_panel = EditorHistoryPanel()
        self.versions_panel = ScheduleVersionsPanel()
        self.local_optimization_panel = LocalOptimizationPanel()

        side_tabs = QTabWidget()
        side_tabs.addTab(self.impact_panel, "Impacto")
        side_tabs.addTab(self.local_optimization_panel, "Mejoras")
        side_tabs.addTab(self.history_panel, "Historial")
        side_tabs.addTab(self.versions_panel, "Versiones")

        splitter = QSplitter()
        splitter.addWidget(self.table)
        splitter.addWidget(side_tabs)
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 1)

        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addWidget(self.status_label)
        layout.addWidget(splitter)

        self.reload_entities()

    def reload_entities(self) -> None:
        current = self.selector.currentData()
        self.selector.blockSignals(True)
        self.selector.clear()

        items = self.service.list_courses() if self.mode == "course" else self.service.list_teachers()
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

        matrix = self.service.course_matrix(entity_id) if self.mode == "course" else self.service.teacher_matrix(entity_id)

        for day in range(1, 6):
            for period in range(1, 7):
                cell = matrix.get((day, period))
                if cell is None:
                    continue

                text = (
                    f"{cell.subject_name}\n{cell.teacher_name}\n{cell.room_name}".strip()
                    if self.mode == "course"
                    else f"{cell.course_code}\n{cell.subject_name}\n{cell.room_name}".strip()
                )

                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(self.COLOR_DEFAULT)
                item.setData(self.SESSION_ID_ROLE, cell.id)
                item.setData(self.DAY_ROLE, day)
                item.setData(self.PERIOD_ROLE, period)
                self.table.setItem(period - 1, day - 1, item)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def _set_empty_cell(self, day: int, period: int) -> None:
        item = QTableWidgetItem("")
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(self.COLOR_DEFAULT)
        item.setData(self.SESSION_ID_ROLE, None)
        item.setData(self.DAY_ROLE, day)
        item.setData(self.PERIOD_ROLE, period)
        self.table.setItem(period - 1, day - 1, item)

    def preview_drag_target(self, source_session_id: int, day: int, period: int) -> None:
        self.clear_live_preview()
        item = self.table.item(period - 1, day - 1)
        if item is None:
            return

        validation = self.live_validator.validate_cell(
            source_session_id=source_session_id,
            target_session_id=item.data(self.SESSION_ID_ROLE),
            day=day,
            period=period,
        )

        if validation.status == "valid":
            item.setBackground(self.COLOR_VALID)
        elif validation.status == "swap":
            item.setBackground(self.COLOR_SWAP)
        elif validation.status == "same":
            item.setBackground(self.COLOR_SAME)

        self.status_label.setText(validation.message)

    def clear_live_preview(self) -> None:
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item is not None:
                    item.setBackground(self.COLOR_DEFAULT)

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
        self.history_panel.add_text(f"Sesión marcada: {self.marked_session_label}")

    def clear_marked_session(self) -> None:
        self.marked_session_id = None
        self.marked_session_label = ""
        self.status_label.setText("Editor: selección cancelada.")
        self.history_panel.add_text("Selección cancelada")

    def move_session_by_drag(self, session_id: int, day: int, period: int) -> None:
        result = self.editor_service.move_session(session_id, day, period)
        self._show_result(result, "Mover sesión")
        if result.success:
            self.load_matrix()

    def swap_sessions_by_drag(self, first_session_id: int, second_session_id: int) -> None:
        result = self.editor_service.swap_sessions(first_session_id, second_session_id)
        self._show_result(result, "Intercambiar sesiones")
        if result.success:
            self.load_matrix()

    def move_marked_session(self, day: int, period: int) -> None:
        if self.marked_session_id is None:
            return
        result = self.editor_service.move_session(self.marked_session_id, day, period)
        self._show_result(result, "Mover sesión marcada")
        if result.success:
            self.clear_marked_session()
            self.load_matrix()

    def swap_marked_session(self, other_session_id: int) -> None:
        if self.marked_session_id is None:
            return
        result = self.editor_service.swap_sessions(self.marked_session_id, int(other_session_id))
        self._show_result(result, "Intercambiar sesión marcada")
        if result.success:
            self.clear_marked_session()
            self.load_matrix()

    def undo_last_action(self) -> None:
        result = self.editor_service.undo()
        self._show_result(result, "Deshacer")
        if result.success:
            self.load_matrix()

    def redo_last_action(self) -> None:
        result = self.editor_service.redo()
        self._show_result(result, "Rehacer")
        if result.success:
            self.load_matrix()

    def _show_result(self, result, action: str = "Acción") -> None:
        self.impact_panel.show_result(result)
        self.local_optimization_panel.analyse_result(result)
        self.history_panel.add_result(action, result)

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
