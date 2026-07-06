from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
    QMessageBox,
)

from pini_desktop.services.substitution_report_service import (
    SubstitutionReportService,
)


class SubstitutionReportDialog(QDialog):
    """
    Diálogo para visualizar y exportar el informe de sustituciones.
    """

    def __init__(self, substitutions=None, parent=None):
        super().__init__(parent)

        self.substitutions = substitutions or []
        self.report_service = SubstitutionReportService()

        self.setWindowTitle("Informe de sustituciones")
        self.resize(1100, 600)

        self._build_ui()
        self._load_data()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Informe de sustituciones")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(9)

        self.table.setHorizontalHeaderLabels([
            "Fecha",
            "Periodo",
            "Profesor ausente",
            "Profesor sustituto",
            "Grupo",
            "Asignatura",
            "Aula",
            "Motivo",
            "Observaciones",
        ])

        layout.addWidget(self.table)

        button_layout = QHBoxLayout()

        self.export_button = QPushButton("Exportar CSV")
        self.close_button = QPushButton("Cerrar")

        self.export_button.clicked.connect(self.export_csv)
        self.close_button.clicked.connect(self.accept)

        button_layout.addStretch()
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)

    def _load_data(self):
        rows = self.report_service.build_report_rows(self.substitutions)

        self.table.setRowCount(len(rows))

        for row_index, row in enumerate(rows):
            values = [
                row["fecha"],
                row["periodo"],
                row["profesor_ausente"],
                row["profesor_sustituto"],
                row["grupo"],
                row["asignatura"],
                row["aula"],
                row["motivo"],
                row["observaciones"],
            ]

            for col_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_index, col_index, item)

        self.table.resizeColumnsToContents()

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar informe de sustituciones",
            "informe_sustituciones.csv",
            "CSV (*.csv)",
        )

        if not path:
            return

        try:
            self.report_service.export_csv(self.substitutions, path)

            QMessageBox.information(
                self,
                "Informe exportado",
                "El informe de sustituciones se ha exportado correctamente.",
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo exportar el informe:\n{error}",
            )