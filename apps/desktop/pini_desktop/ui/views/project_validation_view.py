from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from pini_desktop.services.project_validation_service import (
    ProjectValidationService,
    ValidationSeverity,
)


class ProjectValidationView(QWidget):
    HEADERS = ["Severidad", "Código", "Área", "Mensaje"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = ProjectValidationService()

        self.summary = QLabel("Validación del proyecto")
        self.summary.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        validate_button = QPushButton("Validar proyecto")
        validate_button.clicked.connect(self.load_issues)

        layout = QVBoxLayout(self)
        layout.addWidget(self.summary)
        layout.addWidget(validate_button)
        layout.addWidget(self.table)

        self.load_issues()

    def load_issues(self) -> None:
        issues = self.service.validate()
        self.table.setRowCount(len(issues))

        errors = sum(1 for issue in issues if issue.severity == ValidationSeverity.ERROR)
        warnings = sum(1 for issue in issues if issue.severity == ValidationSeverity.WARNING)

        if errors:
            self.summary.setText(f"Proyecto con {errors} errores y {warnings} avisos.")
        elif warnings:
            self.summary.setText(f"Proyecto sin errores, pero con {warnings} avisos.")
        else:
            self.summary.setText("Proyecto preparado.")

        for row_index, issue in enumerate(issues):
            values = [issue.severity.value, issue.code, issue.area, issue.message]
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignVCenter)
                if issue.severity == ValidationSeverity.ERROR:
                    item.setBackground(Qt.red)
                elif issue.severity == ValidationSeverity.WARNING:
                    item.setBackground(Qt.yellow)
                elif issue.severity == ValidationSeverity.INFO:
                    item.setBackground(Qt.green)
                self.table.setItem(row_index, column_index, item)

        self.table.resizeColumnsToContents()
