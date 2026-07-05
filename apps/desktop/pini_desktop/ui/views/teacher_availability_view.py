from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from pini_desktop.services.availability_service import AvailabilityService, AvailabilityStatus
from pini_desktop.services.teacher_service import TeacherService


class TeacherAvailabilityView(QWidget):
    DAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    STATUS_LABELS = {
        AvailabilityStatus.AVAILABLE: "Disponible",
        AvailabilityStatus.PREFERRED: "Preferente",
        AvailabilityStatus.AVOID: "Evitar",
        AvailabilityStatus.FORBIDDEN: "No disponible",
    }
    LABEL_TO_STATUS = {v: k for k, v in STATUS_LABELS.items()}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.teacher_service = TeacherService()
        self.availability_service = AvailabilityService()

        self.teacher_combo = QComboBox()
        self.teacher_combo.currentIndexChanged.connect(self.load_selected_teacher)

        self.table = QTableWidget()
        self.table.setRowCount(6)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(self.DAYS)
        self.table.setVerticalHeaderLabels([f"P{i}" for i in range(1, 7)])

        save_button = QPushButton("Guardar disponibilidad")
        save_button.clicked.connect(self.save_matrix)

        available_button = QPushButton("Todo disponible")
        available_button.clicked.connect(lambda: self.fill_status(AvailabilityStatus.AVAILABLE))

        forbidden_button = QPushButton("Todo no disponible")
        forbidden_button.clicked.connect(lambda: self.fill_status(AvailabilityStatus.FORBIDDEN))

        top = QHBoxLayout()
        top.addWidget(QLabel("Profesor/a:"))
        top.addWidget(self.teacher_combo)
        top.addStretch()
        top.addWidget(available_button)
        top.addWidget(forbidden_button)
        top.addWidget(save_button)

        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addWidget(self.table)

        self.load_teachers()

    def load_teachers(self) -> None:
        self.teacher_combo.clear()
        for teacher in self.teacher_service.list_teachers():
            self.teacher_combo.addItem(f"{teacher.code} - {teacher.full_name}", teacher.id)
        self.load_selected_teacher()

    def load_selected_teacher(self) -> None:
        teacher_id = self.teacher_combo.currentData()
        if teacher_id is None:
            self.table.clearContents()
            return

        matrix = self.availability_service.get_matrix(teacher_id)
        for day in range(1, 6):
            for period in range(1, 7):
                status = matrix.get((day, period), AvailabilityStatus.AVAILABLE)
                item = QTableWidgetItem(self.STATUS_LABELS[status])
                item.setTextAlignment(Qt.AlignCenter)
                item.setData(Qt.UserRole, status.value)
                self._apply_color(item, status)
                self.table.setItem(period - 1, day - 1, item)

        self.table.resizeColumnsToContents()

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)

    def fill_status(self, status: AvailabilityStatus) -> None:
        for day in range(1, 6):
            for period in range(1, 7):
                item = QTableWidgetItem(self.STATUS_LABELS[status])
                item.setTextAlignment(Qt.AlignCenter)
                item.setData(Qt.UserRole, status.value)
                self._apply_color(item, status)
                self.table.setItem(period - 1, day - 1, item)

    def save_matrix(self) -> None:
        teacher_id = self.teacher_combo.currentData()
        if teacher_id is None:
            QMessageBox.information(self, "Sin profesorado", "Primero crea al menos un profesor.")
            return

        matrix = {}
        for day in range(1, 6):
            for period in range(1, 7):
                item = self.table.item(period - 1, day - 1)
                status = AvailabilityStatus(item.data(Qt.UserRole)) if item else AvailabilityStatus.AVAILABLE
                matrix[(day, period)] = status

        self.availability_service.set_matrix(teacher_id, matrix)
        QMessageBox.information(self, "Guardado", "Disponibilidad guardada.")

    def keyPressEvent(self, event):
        status = None
        if event.text() == "1":
            status = AvailabilityStatus.AVAILABLE
        elif event.text() == "2":
            status = AvailabilityStatus.PREFERRED
        elif event.text() == "3":
            status = AvailabilityStatus.AVOID
        elif event.text() == "4":
            status = AvailabilityStatus.FORBIDDEN

        if status is not None:
            for index in self.table.selectedIndexes():
                item = QTableWidgetItem(self.STATUS_LABELS[status])
                item.setTextAlignment(Qt.AlignCenter)
                item.setData(Qt.UserRole, status.value)
                self._apply_color(item, status)
                self.table.setItem(index.row(), index.column(), item)
            return

        super().keyPressEvent(event)

    def _apply_color(self, item: QTableWidgetItem, status: AvailabilityStatus) -> None:
        if status == AvailabilityStatus.AVAILABLE:
            item.setBackground(Qt.white)
        elif status == AvailabilityStatus.PREFERRED:
            item.setBackground(Qt.green)
        elif status == AvailabilityStatus.AVOID:
            item.setBackground(Qt.yellow)
        elif status == AvailabilityStatus.FORBIDDEN:
            item.setBackground(Qt.red)
