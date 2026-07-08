from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QListWidget, QPushButton, QVBoxLayout, QWidget

from pini_desktop.services.editor.optimization.alternative_apply_service import AlternativeApplyService
from pini_desktop.services.editor.optimization.alternative_generator import AlternativeGenerator


class AlternativesPanel(QWidget):
    alternativeApplied = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.generator = AlternativeGenerator()
        self.apply_service = AlternativeApplyService()
        self.current_alternatives = []

        title = QLabel("Asistente IA · Alternativas")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.summary_label = QLabel("Selecciona una sesión para generar alternativas.")
        self.summary_label.setWordWrap(True)

        self.list_widget = QListWidget()

        apply_button = QPushButton("Aplicar alternativa seleccionada")
        apply_button.clicked.connect(self.apply_selected)

        clear_button = QPushButton("Limpiar alternativas")
        clear_button.clicked.connect(self.clear)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.list_widget)
        layout.addWidget(apply_button)
        layout.addWidget(clear_button)

    def generate_for_session(self, session_id: int, day: int, period: int, current_score: float = 80.0) -> None:
        self.current_alternatives = list(
            self.generator.generate_for_session(
                session_id=session_id,
                current_day=day,
                current_period=period,
                current_score=current_score,
            )
        )
        self.list_widget.clear()

        if not self.current_alternatives:
            self.summary_label.setText("No se han encontrado alternativas.")
            return

        self.summary_label.setText(f"Alternativas encontradas: {len(self.current_alternatives)}")

        for index, alternative in enumerate(self.current_alternatives, start=1):
            star = "⭐ " if index == 1 else ""
            bullets = "\n".join(alternative.bullets)
            self.list_widget.addItem(
                f"{star}{alternative.title} · +{alternative.estimated_delta}\n"
                f"Score estimado: {alternative.estimated_score}\n"
                f"{alternative.explanation}\n"
                f"{bullets}"
            )

    def apply_selected(self):
        row = self.list_widget.currentRow()
        if row < 0 or row >= len(self.current_alternatives):
            self.summary_label.setText("Selecciona una alternativa.")
            return

        result = self.apply_service.apply(self.current_alternatives[row])
        self.summary_label.setText(result.message)

        if result.editor_result is not None:
            self.alternativeApplied.emit(result.editor_result)

    def clear(self):
        self.current_alternatives = []
        self.list_widget.clear()
        self.summary_label.setText("Sin alternativas.")
