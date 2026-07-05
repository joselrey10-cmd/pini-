from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from pini_desktop.services.subject_service import Subject


class SubjectDialog(QDialog):
    def __init__(self, parent=None, subject: Subject | None = None):
        super().__init__(parent)
        self.setWindowTitle("Materia")
        self.subject = subject

        self.code_input = QLineEdit()
        self.name_input = QLineEdit()
        self.speciality_input = QLineEdit()
        self.room_type_input = QLineEdit()

        self.weekly_sessions_input = QSpinBox()
        self.weekly_sessions_input.setRange(1, 10)
        self.weekly_sessions_input.setValue(1)

        self.max_consecutive_input = QSpinBox()
        self.max_consecutive_input.setRange(1, 3)
        self.max_consecutive_input.setValue(1)

        self.double_session_input = QCheckBox("Permitir doble sesión")

        if subject is not None:
            self.code_input.setText(subject.code)
            self.name_input.setText(subject.name)
            self.weekly_sessions_input.setValue(subject.weekly_sessions)
            self.speciality_input.setText(subject.required_speciality)
            self.room_type_input.setText(subject.room_type)
            self.max_consecutive_input.setValue(subject.max_consecutive)
            self.double_session_input.setChecked(subject.allows_double_session)

        form = QFormLayout()
        form.addRow("Código", self.code_input)
        form.addRow("Nombre", self.name_input)
        form.addRow("Sesiones semanales", self.weekly_sessions_input)
        form.addRow("Especialidad requerida", self.speciality_input)
        form.addRow("Tipo de aula", self.room_type_input)
        form.addRow("Máximo consecutivas", self.max_consecutive_input)
        form.addRow("", self.double_session_input)

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

    def get_subject(self) -> Subject:
        return Subject(
            id=self.subject.id if self.subject else None,
            code=self.code_input.text().strip().upper(),
            name=self.name_input.text().strip(),
            weekly_sessions=self.weekly_sessions_input.value(),
            required_speciality=self.speciality_input.text().strip(),
            room_type=self.room_type_input.text().strip(),
            max_consecutive=self.max_consecutive_input.value(),
            allows_double_session=self.double_session_input.isChecked(),
        )

    def _accept_if_valid(self) -> None:
        subject = self.get_subject()
        if not subject.code or not subject.name:
            QMessageBox.warning(self, "Datos incompletos", "Rellena código y nombre.")
            return
        self.accept()
