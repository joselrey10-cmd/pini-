from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QTextEdit, QVBoxLayout

from pini_desktop.services.editor.optimization.predictive_report import PredictiveSimulationReport


class PredictiveSimulationDialog(QDialog):
    def __init__(self, predictive_score, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Simulación predictiva")
        self.resize(620, 500)

        title = QLabel("Impacto futuro estimado")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.text.setPlainText(PredictiveSimulationReport().build_text(predictive_score))

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.text)
        layout.addWidget(buttons)
