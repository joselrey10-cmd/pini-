from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from pini_desktop.services.educacyl_service import DesktopEducaCyLService


class EducaCyLHistoryView(QWidget):
    HEADERS = ["ID", "Fecha", "Origen", "Proveedor", "Profesores", "Cursos", "Materias", "Aulas", "Altas", "Cambios", "Bajas", "Avisos"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = DesktopEducaCyLService()

        title = QLabel("Historial de sincronizaciones EducaCyL")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        refresh_button = QPushButton("Actualizar")
        refresh_button.clicked.connect(self.load_history)

        clear_button = QPushButton("Limpiar historial")
        clear_button.clicked.connect(self.clear_history)

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(refresh_button)
        layout.addWidget(clear_button)
        layout.addWidget(self.table)

        self.load_history()

    def load_history(self):
        records = self.service.list_history()
        self.table.setRowCount(len(records))

        for row, item in enumerate(records):
            values = [
                item.id,
                item.created_at,
                item.source,
                item.provider,
                item.teachers,
                item.courses,
                item.subjects,
                item.rooms,
                item.created,
                item.updated,
                item.deleted,
                "; ".join(item.warnings),
            ]
            for col, value in enumerate(values):
                cell = QTableWidgetItem(str(value))
                if col in {0, 4, 5, 6, 7, 8, 9, 10}:
                    cell.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, cell)

        self.table.resizeColumnsToContents()

    def clear_history(self):
        self.service.clear_history()
        self.load_history()
