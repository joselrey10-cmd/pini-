from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QTextEdit, QVBoxLayout


class AlternativePreviewDialog(QDialog):
    def __init__(self, preview_text: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Previsualizar alternativa")
        self.resize(480, 360)

        title = QLabel("Revisa la alternativa antes de aplicarla")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.text.setPlainText(preview_text)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.text)
        layout.addWidget(buttons)
