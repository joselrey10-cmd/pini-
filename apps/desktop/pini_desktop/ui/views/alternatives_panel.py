from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QListWidget, QPushButton, QTextEdit, QVBoxLayout, QWidget

from pini_desktop.services.editor.optimization.alternative_apply_service import AlternativeApplyService
from pini_desktop.services.editor.optimization.alternative_comparator import AlternativeComparator
from pini_desktop.services.editor.optimization.alternative_generator import AlternativeGenerator
from pini_desktop.services.editor.optimization.alternative_preview import AlternativePreviewService
from pini_desktop.ui.views.alternative_preview_dialog import AlternativePreviewDialog


class AlternativesPanel(QWidget):
    alternativeApplied = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.generator = AlternativeGenerator()
        self.comparator = AlternativeComparator()
        self.preview_service = AlternativePreviewService()
        self.apply_service = AlternativeApplyService()
        self.current_alternatives = []
        self.current_comparison = None

        title = QLabel("Asistente IA · Alternativas")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.summary_label = QLabel("Selecciona una sesión para generar alternativas.")
        self.summary_label.setWordWrap(True)

        self.recommendation_box = QTextEdit()
        self.recommendation_box.setReadOnly(True)
        self.recommendation_box.setFixedHeight(110)

        self.list_widget = QListWidget()

        preview_button = QPushButton("Previsualizar alternativa")
        preview_button.clicked.connect(self.preview_selected)

        apply_button = QPushButton("Aplicar alternativa seleccionada")
        apply_button.clicked.connect(self.apply_selected)

        clear_button = QPushButton("Limpiar alternativas")
        clear_button.clicked.connect(self.clear)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.recommendation_box)
        layout.addWidget(self.list_widget)
        layout.addWidget(preview_button)
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
        self.current_comparison = self.comparator.compare(self.current_alternatives)
        self.list_widget.clear()

        if not self.current_alternatives:
            self.summary_label.setText("No se han encontrado alternativas.")
            self.recommendation_box.setPlainText("")
            return

        self.summary_label.setText(f"Alternativas encontradas: {len(self.current_alternatives)}")
        self._show_best_recommendation()

        comparison_by_title = {item.alternative.title: item for item in self.current_comparison.items}

        for alternative in self.current_alternatives:
            comparison_item = comparison_by_title.get(alternative.title)
            rank = comparison_item.rank if comparison_item else "?"
            recommendation = comparison_item.recommendation if comparison_item else ""
            strengths = "\n".join(f"  {item}" for item in (comparison_item.strengths if comparison_item else ()))
            weaknesses = "\n".join(f"  {item}" for item in (comparison_item.weaknesses if comparison_item else ()))

            self.list_widget.addItem(
                f"#{rank} · {alternative.title} · +{alternative.estimated_delta}\n"
                f"Score estimado: {alternative.estimated_score}\n"
                f"{recommendation}\n"
                f"Fortalezas:\n{strengths}\n"
                f"Aspectos a revisar:\n{weaknesses}"
            )

    def _show_best_recommendation(self):
        if not self.current_comparison or not self.current_comparison.best:
            self.recommendation_box.setPlainText("")
            return

        best = self.current_comparison.best
        text = [
            "Mejor alternativa recomendada",
            f"{best.alternative.title}",
            f"Mejora estimada: +{best.alternative.estimated_delta}",
            best.recommendation,
            "",
            "Por qué:",
        ]
        text.extend(f"• {item}" for item in best.strengths)
        if best.weaknesses:
            text.append("")
            text.append("Revisar:")
            text.extend(f"• {item}" for item in best.weaknesses)

        self.recommendation_box.setPlainText("\n".join(text))

    def selected_alternative(self):
        row = self.list_widget.currentRow()
        if row < 0 or row >= len(self.current_alternatives):
            self.summary_label.setText("Selecciona una alternativa.")
            return None
        return self.current_alternatives[row]

    def preview_selected(self):
        alternative = self.selected_alternative()
        if alternative is None:
            return
        dialog = AlternativePreviewDialog(self.preview_service.build_text(alternative), self)
        dialog.exec()

    def apply_selected(self):
        alternative = self.selected_alternative()
        if alternative is None:
            return

        dialog = AlternativePreviewDialog(self.preview_service.build_text(alternative), self)
        if dialog.exec() != dialog.Accepted:
            self.summary_label.setText("Aplicación cancelada.")
            return

        result = self.apply_service.apply(alternative)
        self.summary_label.setText(result.message)

        if result.editor_result is not None:
            self.alternativeApplied.emit(result.editor_result)

    def clear(self):
        self.current_alternatives = []
        self.current_comparison = None
        self.list_widget.clear()
        self.recommendation_box.setPlainText("")
        self.summary_label.setText("Sin alternativas.")
