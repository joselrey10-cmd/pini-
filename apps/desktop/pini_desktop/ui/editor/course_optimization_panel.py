from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class CourseOptimizationPanel(QWidget):
    optimize_course_requested = Signal(int)

    def __init__(self):
        super().__init__()

        self.course_id = None

        layout = QVBoxLayout(self)

        self.title = QLabel("Optimización de curso")
        self.course_label = QLabel("Curso no seleccionado")
        self.summary_label = QLabel("")
        self.button = QPushButton("Optimizar curso")
        self.button.setEnabled(False)

        self.button.clicked.connect(self._emit_optimize)

        layout.addWidget(self.title)
        layout.addWidget(self.course_label)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.button)

    def set_course(self, course_id: int, course_name: str = ""):
        self.course_id = course_id
        text = f"Curso seleccionado: {course_id}"
        if course_name:
            text += f" · {course_name}"
        self.course_label.setText(text)
        self.button.setEnabled(True)

    def set_result(self, result):
        self.summary_label.setText(
            f"{result.summary} Mejor mejora: {result.best_delta:+.1f}"
        )

    def _emit_optimize(self):
        if self.course_id is not None:
            self.optimize_course_requested.emit(self.course_id)