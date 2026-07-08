from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QTextEdit, QVBoxLayout

from pini_desktop.services.editor.optimization.sequence_detailed_report import SequenceDetailedReport


class SequenceReportDialog(QDialog):
    def __init__(self, sequence_score, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Informe de cadena IA")
        self.resize(620, 500)

        title = QLabel("Informe detallado de cadena IA")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.text.setPlainText(SequenceDetailedReport().build_text(sequence_score))

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.text)
        layout.addWidget(buttons)
