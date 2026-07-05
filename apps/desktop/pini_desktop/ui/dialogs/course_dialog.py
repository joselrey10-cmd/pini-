from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from pini_desktop.services.course_service import Course


class CourseDialog(QDialog):
    def __init__(self, parent=None, course: Course | None = None):
        super().__init__(parent)
        self.setWindowTitle("Curso")
        self.course = course

        self.code_input = QLineEdit()

        self.stage_input = QComboBox()
        self.stage_input.addItems(["Primaria", "Infantil"])

        self.level_input = QSpinBox()
        self.level_input.setRange(1, 6)
        self.level_input.setValue(1)

        self.group_input = QLineEdit()
        self.group_input.setMaxLength(2)

        self.students_input = QSpinBox()
        self.students_input.setRange(1, 35)
        self.students_input.setValue(25)

        if course is not None:
            self.code_input.setText(course.code)
            index = self.stage_input.findText(course.stage)
            if index >= 0:
                self.stage_input.setCurrentIndex(index)
            self.level_input.setValue(course.level)
            self.group_input.setText(course.group_name)
            self.students_input.setValue(course.students)

        form = QFormLayout()
        form.addRow("Código", self.code_input)
        form.addRow("Etapa", self.stage_input)
        form.addRow("Nivel", self.level_input)
        form.addRow("Grupo", self.group_input)
        form.addRow("Nº alumnado", self.students_input)

        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self._accept_if_valid)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)

        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addLayout(buttons)

    def get_course(self) -> Course:
        return Course(
            id=self.course.id if self.course else None,
            code=self.code_input.text().strip(),
            stage=self.stage_input.currentText().strip(),
            level=self.level_input.value(),
            group_name=self.group_input.text().strip().upper(),
            students=self.students_input.value(),
            tutor_teacher_id=self.course.tutor_teacher_id if self.course else None,
        )

    def _accept_if_valid(self) -> None:
        course = self.get_course()
        if not course.code or not course.group_name:
            QMessageBox.warning(self, "Datos incompletos", "Rellena código y grupo.")
            return
        self.accept()
