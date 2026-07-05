from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QMessageBox, QPushButton, QStatusBar, QTabWidget, QVBoxLayout, QWidget

from pini_desktop.ui.views.course_subjects_view import CourseSubjectsView
from pini_desktop.ui.views.courses_view import CoursesView
from pini_desktop.ui.views.project_validation_view import ProjectValidationView
from pini_desktop.ui.views.rooms_view import RoomsView
from pini_desktop.ui.views.schedule_matrix_view import CourseScheduleView, TeacherScheduleView
from pini_desktop.ui.views.schedule_view import ScheduleView
from pini_desktop.ui.views.subjects_view import SubjectsView
from pini_desktop.ui.views.teacher_availability_view import TeacherAvailabilityView
from pini_desktop.ui.views.teachers_view import TeachersView
from pini_desktop.ui.views.timetable_settings_view import TimetableSettingsView


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Pini 0.1 - Planificador Inteligente")
        self.resize(1100, 720)
        self.tabs = QTabWidget()
        self._build_menu()
        self._build_central_widget()
        self._build_status_bar()

    def _build_menu(self) -> None:
        menu = self.menuBar()
        file_menu = menu.addMenu("Archivo")
        file_menu.addAction("Nuevo proyecto", self._show_home)
        file_menu.addAction("Abrir proyecto", self._not_implemented)
        file_menu.addAction("Guardar", self._not_implemented)
        file_menu.addSeparator()
        file_menu.addAction("Salir", self.close)

        center_menu = menu.addMenu("Centro")
        center_menu.addAction("Configuración", self._not_implemented)
        center_menu.addAction("Calendario", self._not_implemented)
        center_menu.addAction("Horario general", self._show_timetable_settings)

        data_menu = menu.addMenu("Datos")
        data_menu.addAction("Profesores", self._show_teachers)
        data_menu.addAction("Disponibilidad profesorado", self._show_teacher_availability)
        data_menu.addAction("Cursos", self._show_courses)
        data_menu.addAction("Materias", self._show_subjects)
        data_menu.addAction("Aulas", self._show_rooms)
        data_menu.addSeparator()
        data_menu.addAction("Materias por curso", self._show_course_subjects)

        schedule_menu = menu.addMenu("Horarios")
        schedule_menu.addAction("Validar proyecto", self._show_project_validation)
        schedule_menu.addAction("Generar", self._show_schedule)
        schedule_menu.addAction("Horario por curso", self._show_course_schedule)
        schedule_menu.addAction("Horario por profesor", self._show_teacher_schedule)
        schedule_menu.addAction("Optimizar", self._not_implemented)

        reports_menu = menu.addMenu("Informes")
        reports_menu.addAction("Horario por profesor", self._show_teacher_schedule)
        reports_menu.addAction("Horario por curso", self._show_course_schedule)
        reports_menu.addAction("Exportar PDF", self._not_implemented)
        reports_menu.addAction("Exportar Excel", self._not_implemented)

        help_menu = menu.addMenu("Ayuda")
        help_menu.addAction("Acerca de Pini", self._about)

    def _build_central_widget(self) -> None:
        self.tabs.addTab(self._home_widget(), "Inicio")
        self.setCentralWidget(self.tabs)

    def _home_widget(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("PINI")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 42px; font-weight: bold;")

        subtitle = QLabel("Planificador Inteligente de Horarios Escolares")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 18px;")

        school = QLabel("CEIP Tierra de Pinares")
        school.setAlignment(Qt.AlignCenter)
        school.setStyleSheet("font-size: 16px; margin-bottom: 24px;")

        buttons = [
            ("Horario general del centro", self._show_timetable_settings),
            ("Gestionar profesores", self._show_teachers),
            ("Disponibilidad profesorado", self._show_teacher_availability),
            ("Gestionar cursos", self._show_courses),
            ("Gestionar materias", self._show_subjects),
            ("Gestionar aulas", self._show_rooms),
            ("Asignar materias a cursos", self._show_course_subjects),
            ("Validar proyecto", self._show_project_validation),
            ("Generar horario básico", self._show_schedule),
            ("Ver horario por curso", self._show_course_schedule),
            ("Ver horario por profesor", self._show_teacher_schedule),
        ]

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(school)

        for text, handler in buttons:
            button = QPushButton(text)
            button.setMinimumWidth(280)
            button.clicked.connect(handler)
            layout.addWidget(button, alignment=Qt.AlignCenter)

        return container

    def _build_status_bar(self) -> None:
        status = QStatusBar()
        status.showMessage("Listo")
        self.setStatusBar(status)

    def _show_home(self) -> None:
        self.tabs.setCurrentIndex(0)

    def _show_teachers(self) -> None:
        self._open_tab("Profesores", TeachersView)

    def _show_teacher_availability(self) -> None:
        self._open_tab("Disponibilidad profesorado", TeacherAvailabilityView)

    def _show_courses(self) -> None:
        self._open_tab("Cursos", CoursesView)

    def _show_subjects(self) -> None:
        self._open_tab("Materias", SubjectsView)

    def _show_rooms(self) -> None:
        self._open_tab("Aulas", RoomsView)

    def _show_course_subjects(self) -> None:
        self._open_tab("Materias por curso", CourseSubjectsView)

    def _show_timetable_settings(self) -> None:
        self._open_tab("Horario general", TimetableSettingsView)

    def _show_project_validation(self) -> None:
        self._open_tab("Validación", ProjectValidationView)

    def _show_schedule(self) -> None:
        self._open_tab("Horario generado", ScheduleView)

    def _show_course_schedule(self) -> None:
        self._open_tab("Horario por curso", CourseScheduleView)

    def _show_teacher_schedule(self) -> None:
        self._open_tab("Horario por profesor", TeacherScheduleView)

    def _open_tab(self, title: str, view_class) -> None:
        index = self._find_tab(title)
        if index == -1:
            self.tabs.addTab(view_class(self), title)
            index = self.tabs.count() - 1
        self.tabs.setCurrentIndex(index)
        self.statusBar().showMessage(title)

    def _find_tab(self, title: str) -> int:
        for index in range(self.tabs.count()):
            if self.tabs.tabText(index) == title:
                return index
        return -1

    def _about(self) -> None:
        QMessageBox.information(self, "Acerca de Pini", "Pini 0.1\\nPlanificador Inteligente de Horarios Escolares.")

    def _not_implemented(self) -> None:
        QMessageBox.information(self, "Pini", "Esta función se implementará en los próximos commits.")
