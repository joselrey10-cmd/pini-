from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from pini_desktop.services.substitution_report_service import SubstitutionReportService


class SubstitutionReportView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = SubstitutionReportService()

        title = QLabel("Informes de sustituciones")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.summary_label = QLabel()
        self.summary_label.setWordWrap(True)

        refresh_button = QPushButton("Actualizar resumen")
        refresh_button.clicked.connect(self.load_summary)

        export_button = QPushButton("Exportar sustituciones a Excel")
        export_button.clicked.connect(self.export_excel)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.summary_label)
        layout.addWidget(refresh_button)
        layout.addWidget(export_button)
        layout.addStretch()

        self.load_summary()

    def load_summary(self):
        summary = self.service.summary()
        self.summary_label.setText(
            f"Total: {summary.total}\n"
            f"Planificadas: {summary.planned}\n"
            f"Realizadas: {summary.done}\n"
            f"Canceladas: {summary.cancelled}"
        )

    def export_excel(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar informe de sustituciones",
            str(Path.home() / "sustituciones_pini.xlsx"),
            "Excel (*.xlsx)",
        )
        if not path:
            return

        exported = self.service.export_excel(path)
        QMessageBox.information(
            self,
            "Informe exportado",
            f"Informe guardado en:\n{exported}",
        )
