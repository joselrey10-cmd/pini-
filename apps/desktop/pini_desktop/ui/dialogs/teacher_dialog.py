from PySide6.QtWidgets import QDialog, QFormLayout, QHBoxLayout, QLineEdit, QMessageBox, QPushButton, QSpinBox, QVBoxLayout
from pini_desktop.services.teacher_service import Teacher

class TeacherDialog(QDialog):
    def __init__(self, parent=None, teacher: Teacher | None = None):
        super().__init__(parent)
        self.setWindowTitle("Profesor")
        self.teacher = teacher

        self.code_input = QLineEdit()
        self.name_input = QLineEdit()
        self.surname_input = QLineEdit()
        self.speciality_input = QLineEdit()
        self.weekly_hours_input = QSpinBox()
        self.weekly_hours_input.setRange(1, 40)
        self.weekly_hours_input.setValue(25)
        self.max_daily_input = QSpinBox()
        self.max_daily_input.setRange(1, 8)
        self.max_daily_input.setValue(5)

        if teacher is not None:
            self.code_input.setText(teacher.code)
            self.name_input.setText(teacher.name)
            self.surname_input.setText(teacher.surname)
            self.speciality_input.setText(teacher.speciality)
            self.weekly_hours_input.setValue(teacher.weekly_hours)
            self.max_daily_input.setValue(teacher.max_daily_sessions)

        form = QFormLayout()
        form.addRow("Código", self.code_input)
        form.addRow("Nombre", self.name_input)
        form.addRow("Apellidos", self.surname_input)
        form.addRow("Especialidad", self.speciality_input)
        form.addRow("Horas semanales", self.weekly_hours_input)
        form.addRow("Máximo sesiones diarias", self.max_daily_input)

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

    def get_teacher(self) -> Teacher:
        return Teacher(
            id=self.teacher.id if self.teacher else None,
            code=self.code_input.text().strip(),
            name=self.name_input.text().strip(),
            surname=self.surname_input.text().strip(),
            speciality=self.speciality_input.text().strip(),
            weekly_hours=self.weekly_hours_input.value(),
            max_daily_sessions=self.max_daily_input.value(),
        )

    def _accept_if_valid(self) -> None:
        teacher = self.get_teacher()
        if not teacher.code or not teacher.name or not teacher.surname or not teacher.speciality:
            QMessageBox.warning(self, "Datos incompletos", "Rellena código, nombre, apellidos y especialidad.")
            return
        self.accept()
