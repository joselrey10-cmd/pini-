from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QListWidget, QPushButton, QVBoxLayout, QWidget

from pini_desktop.services.editor.optimization.local_optimizer import LocalOptimizationService
from pini_desktop.services.editor.optimization.suggestion_service import EditorSuggestionService


class LocalOptimizationPanel(QWidget):
    suggestionApplied = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = LocalOptimizationService()
        self.suggestion_service = EditorSuggestionService()
        self.current_suggestions = []

        title = QLabel("Optimización local")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.summary_label = QLabel("Sin sugerencias todavía.")
        self.summary_label.setWordWrap(True)

        self.list_widget = QListWidget()

        apply_button = QPushButton("Aplicar sugerencia seleccionada")
        apply_button.clicked.connect(self.apply_selected)

        clear_button = QPushButton("Limpiar sugerencias")
        clear_button.clicked.connect(self.clear)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.list_widget)
        layout.addWidget(apply_button)
        layout.addWidget(clear_button)

    def analyse_result(self, result) -> None:
        analysis = self.service.analyse_after_move(result)
        self.current_suggestions = list(analysis.suggestions)
        self.list_widget.clear()

        if not analysis.has_suggestions:
            self.summary_label.setText("No hay sugerencias de optimización local.")
            return

        self.summary_label.setText(
            f"Sugerencias encontradas: {len(analysis.suggestions)} · Mejor delta estimado: {analysis.best_delta}"
        )

        for suggestion in analysis.suggestions:
            self.list_widget.addItem(
                f"{suggestion.title} · +{suggestion.estimated_delta}\n{suggestion.description}"
            )

    def apply_selected(self):
        row = self.list_widget.currentRow()
        if row < 0 or row >= len(self.current_suggestions):
            self.summary_label.setText("Selecciona una sugerencia.")
            return

        result = self.suggestion_service.apply(self.current_suggestions[row])
        self.summary_label.setText(result.message)

        if result.editor_result is not None:
            self.suggestionApplied.emit(result.editor_result)

    def clear(self):
        self.summary_label.setText("Sin sugerencias todavía.")
        self.list_widget.clear()
        self.current_suggestions = []
