from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QTextEdit, QVBoxLayout

from pini_desktop.services.editor.optimization.predictive_dashboard_report import PredictiveDashboardReport


class PredictiveDashboardDialog(QDialog):
    def __init__(self, predictive_scores, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resumen predictivo")
        self.resize(650, 500)

        title = QLabel("Resumen predictivo de cadenas IA")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.text.setPlainText(PredictiveDashboardReport().build_text(predictive_scores))

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.text)
        layout.addWidget(buttons)
