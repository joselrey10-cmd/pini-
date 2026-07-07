from PySide6.QtWidgets import QLabel, QListWidget, QPushButton, QVBoxLayout, QWidget

from pini_desktop.services.editor.optimization.alternative_generator import AlternativeGenerator


class AlternativesPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.generator = AlternativeGenerator()
        self.current_alternatives = []

        title = QLabel("Alternativas inteligentes")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.summary_label = QLabel("Selecciona una sesión para generar alternativas.")
        self.summary_label.setWordWrap(True)

        self.list_widget = QListWidget()

        clear_button = QPushButton("Limpiar alternativas")
        clear_button.clicked.connect(self.clear)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.list_widget)
        layout.addWidget(clear_button)

    def generate_for_session(self, session_id: int, day: int, period: int) -> None:
        self.current_alternatives = list(
            self.generator.generate_for_session(session_id, day, period)
        )
        self.list_widget.clear()

        if not self.current_alternatives:
            self.summary_label.setText("No se han encontrado alternativas.")
            return

        self.summary_label.setText(f"Alternativas encontradas: {len(self.current_alternatives)}")
        for alternative in self.current_alternatives:
            self.list_widget.addItem(
                f"{alternative.title} · +{alternative.estimated_delta}\n{alternative.explanation}"
            )

    def clear(self):
        self.current_alternatives = []
        self.list_widget.clear()
        self.summary_label.setText("Sin alternativas.")
