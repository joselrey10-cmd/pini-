from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QTextEdit, QVBoxLayout


class ZonePlanPreviewDialog(QDialog):
    def __init__(self, plan, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Previsualizar plan de mejora")
        self.resize(520, 420)

        title = QLabel("Plan de mejora por zonas")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        lines = [
            f"Zona: {plan.zone_label}",
            f"Mejora estimada acumulada: +{plan.estimated_delta}",
            "",
            "Acciones:",
        ]

        for action in plan.actions:
            lines.append(
                f"{action.order}. {action.title} · sesión {action.session_id} "
                f"→ día {action.day}, periodo {action.period} · +{action.estimated_delta}"
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
