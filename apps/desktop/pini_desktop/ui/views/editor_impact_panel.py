from PySide6.QtWidgets import QLabel, QTextEdit, QVBoxLayout, QWidget


class EditorImpactPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        title = QLabel("Impacto del cambio")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.score_label = QLabel("Score: —")
        self.score_label.setStyleSheet("font-size: 14px;")

        self.details = QTextEdit()
        self.details.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.score_label)
        layout.addWidget(self.details)

    def clear(self):
        self.score_label.setText("Score: —")
        self.details.setPlainText("")

    def show_result(self, result):
        old_score = getattr(result, "old_score", None)
        new_score = getattr(result, "new_score", None)

        if old_score is not None and new_score is not None:
            delta = round(float(new_score) - float(old_score), 2)
            sign = "+" if delta > 0 else ""
            self.score_label.setText(f"Score: {old_score} → {new_score} ({sign}{delta})")
        elif new_score is not None:
            self.score_label.setText(f"Score: {new_score}")
        else:
            self.score_label.setText("Score: —")

        lines = []
        lines.append("Resultado: correcto" if result.success else "Resultado: no aplicado")

        if result.messages:
            lines.append("")
            lines.append("Mensajes:")
            lines.extend(f"• {message}" for message in result.messages)

        if result.warnings:
            lines.append("")
            lines.append("Avisos:")
            lines.extend(f"• {warning}" for warning in result.warnings)

        affected = getattr(result, "affected_entities", None)
        if affected:
            lines.append("")
            lines.append("Entidades afectadas:")
            for key, values in affected.items():
                if values:
                    lines.append(f"• {key}: {', '.join(str(v) for v in values)}")

        self.details.setPlainText("\n".join(lines))
