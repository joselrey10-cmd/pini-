from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QTextEdit, QVBoxLayout

class SequencePreviewDialog(QDialog):
    def __init__(self, sequence_score, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Previsualizar cadena de movimientos")
        self.resize(560, 430)

        title = QLabel("Cadena recomendada")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        lines = [
            f"Recomendación: {sequence_score.recommendation}",
            f"Score de cadena: {sequence_score.score}",
            f"Riesgo estimado: {sequence_score.risk}",
            f"Mejora acumulada: +{sequence_score.sequence.estimated_delta}",
            "",
            "Pasos:",
        ]
        for step in sequence_score.sequence.steps:
            lines.append(
                f"{step.order}. {step.title} · sesión {step.session_id} "
                f"→ día {step.day}, periodo {step.period} · +{step.estimated_delta}"
            )

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.text.setPlainText("\n".join(lines))

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.text)
        layout.addWidget(buttons)
