from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class TeacherOptimizationPanel(QWidget):
    optimize_teacher_requested = Signal(int)

    def __init__(self):
        super().__init__()

        self.teacher_id = None

        layout = QVBoxLayout(self)

        self.title = QLabel("Optimización de profesor")
        self.teacher_label = QLabel("Profesor no seleccionado")
        self.summary_label = QLabel("")
        self.button = QPushButton("Optimizar profesor")
        self.button.setEnabled(False)

        self.button.clicked.connect(self._emit_optimize)

        layout.addWidget(self.title)
        layout.addWidget(self.teacher_label)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.button)

    def set_teacher(self, teacher_id: int, teacher_name: str = ""):
        self.teacher_id = teacher_id
        text = f"Profesor seleccionado: {teacher_id}"
        if teacher_name:
            text += f" · {teacher_name}"
        self.teacher_label.setText(text)
        self.button.setEnabled(True)

    def set_result(self, result):
        self.summary_label.setText(
            f"{result.summary} Mejor mejora: {result.best_delta:+.1f}"
        )

    def _emit_optimize(self):
        if self.teacher_id is not None:
            self.optimize_teacher_requested.emit(self.teacher_id)