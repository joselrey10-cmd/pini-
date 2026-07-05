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

from pini_desktop.services.course_service import CourseService
from pini_desktop.services.course_subject_service import CourseSubject
from pini_desktop.services.subject_service import SubjectService
from pini_desktop.services.teacher_service import TeacherService


class CourseSubjectDialog(QDialog):
    def __init__(self, parent=None, assignment: CourseSubject | None = None):
        super().__init__(parent)
        self.setWindowTitle("Asignar materia a curso")
        self.assignment = assignment

        self.course_service = CourseService()
        self.subject_service = SubjectService()
        self.teacher_service = TeacherService()

        self.courses = self.course_service.list_courses()
        self.subjects = self.subject_service.list_subjects()
        self.teachers = self.teacher_service.list_teachers()

        self.course_input = QComboBox()
        for course in self.courses:
            self.course_input.addItem(course.code, course.id)

        self.subject_input = QComboBox()
        for subject in self.subjects:
            self.subject_input.addItem(f"{subject.code} - {subject.name}", subject.id)

        self.teacher_input = QComboBox()
        self.teacher_input.addItem("(Sin profesor preferente)", None)
        for teacher in self.teachers:
            self.teacher_input.addItem(f"{teacher.code} - {teacher.full_name}", teacher.id)

        self.weekly_sessions_input = QSpinBox()
        self.weekly_sessions_input.setRange(1, 10)
        self.weekly_sessions_input.setValue(1)

        self.room_type_input = QLineEdit()
        self.notes_input = QLineEdit()

        if assignment is not None:
            self._select_combo_data(self.course_input, assignment.course_id)
            self._select_combo_data(self.subject_input, assignment.subject_id)
            self._select_combo_data(self.teacher_input, assignment.preferred_teacher_id)
            self.weekly_sessions_input.setValue(assignment.weekly_sessions)
            self.room_type_input.setText(assignment.required_room_type)
            self.notes_input.setText(assignment.notes)

        form = QFormLayout()
        form.addRow("Curso", self.course_input)
        form.addRow("Materia", self.subject_input)
        form.addRow("Sesiones semanales", self.weekly_sessions_input)
        form.addRow("Profesor preferente", self.teacher_input)
        form.addRow("Tipo de aula requerida", self.room_type_input)
        form.addRow("Notas", self.notes_input)

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

    def get_assignment(self) -> CourseSubject:
        return CourseSubject(
            id=self.assignment.id if self.assignment else None,
            course_id=self.course_input.currentData(),
            subject_id=self.subject_input.currentData(),
            weekly_sessions=self.weekly_sessions_input.value(),
            preferred_teacher_id=self.teacher_input.currentData(),
            required_room_type=self.room_type_input.text().strip(),
            notes=self.notes_input.text().strip(),
        )

    def _accept_if_valid(self) -> None:
        if self.course_input.currentData() is None or self.subject_input.currentData() is None:
            QMessageBox.warning(self, "Datos incompletos", "Debe existir al menos un curso y una materia.")
            return
        self.accept()

    def _select_combo_data(self, combo: QComboBox, value) -> None:
        for index in range(combo.count()):
            if combo.itemData(index) == value:
                combo.setCurrentIndex(index)
                return
