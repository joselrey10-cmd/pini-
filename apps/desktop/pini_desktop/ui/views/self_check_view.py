from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from pini_desktop.services.self_check_service import SelfCheckService


class SelfCheckView(QWidget):
    HEADERS = ["Área", "Estado", "Mensaje"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = SelfCheckService()

        title = QLabel("Comprobación y reparación de Pini")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        description = QLabel(
            "Comprueba si la base de datos y la interfaz tienen integrados los módulos principales."
        )
        description.setWordWrap(True)

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        check_button = QPushButton("Comprobar")
        check_button.clicked.connect(self.run_checks)

        repair_button = QPushButton("Reparar base de datos")
        repair_button.clicked.connect(self.repair_database)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(check_button)
        layout.addWidget(repair_button)
        layout.addWidget(self.table)

        self.run_checks()

    def run_checks(self):
        self._load_items(self.service.run_checks())

    def repair_database(self):
        items = self.service.repair_database()
        self._load_items(items)
        QMessageBox.information(self, "Reparación", "Base de datos revisada y reparada.")

    def _load_items(self, items):
        self.table.setRowCount(len(items))
        for row_index, item in enumerate(items):
            values = [item.area, item.status, item.message]
            for col_index, value in enumerate(values):
                cell = QTableWidgetItem(str(value))
                cell.setTextAlignment(Qt.AlignVCenter)
                self.table.setItem(row_index, col_index, cell)
        self.table.resizeColumnsToContents()
