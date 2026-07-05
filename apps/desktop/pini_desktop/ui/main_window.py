from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QMessageBox, QPushButton, QStatusBar, QTabWidget, QVBoxLayout, QWidget

from pini_desktop.ui.views.course_subjects_view import CourseSubjectsView
from pini_desktop.ui.views.courses_view import CoursesView
from pini_desktop.ui.views.rooms_view import RoomsView
from pini_desktop.ui.views.subjects_view import SubjectsView
from pini_desktop.ui.views.teachers_view import TeachersView


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
        center_menu.addAction("Horario general", self._not_implemented)

        data_menu = menu.addMenu("Datos")
        data_menu.addAction("Profesores", self._show_teachers)
        data_menu.addAction("Cursos", self._show_courses)
        data_menu.addAction("Materias", self._show_subjects)
        data_menu.addAction("Aulas", self._show_rooms)
        data_menu.addSeparator()
        data_menu.addAction("Materias por curso", self._show_course_subjects)

        schedule_menu = menu.addMenu("Horarios")
        schedule_menu.addAction("Generar", self._not_implemented)
        schedule_menu.addAction("Validar", self._not_implemented)
        schedule_menu.addAction("Optimizar", self._not_implemented)

        reports_menu = menu.addMenu("Informes")
        reports_menu.addAction("Horario por profesor", self._not_implemented)
        reports_menu.addAction("Horario por curso", self._not_implemented)
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

        teachers_button = QPushButton("Gestionar profesores")
        teachers_button.setMinimumWidth(260)
        teachers_button.clicked.connect(self._show_teachers)

        courses_button = QPushButton("Gestionar cursos")
        courses_button.setMinimumWidth(260)
        courses_button.clicked.connect(self._show_courses)

        subjects_button = QPushButton("Gestionar materias")
        subjects_button.setMinimumWidth(260)
        subjects_button.clicked.connect(self._show_subjects)

        rooms_button = QPushButton("Gestionar aulas")
        rooms_button.setMinimumWidth(260)
        rooms_button.clicked.connect(self._show_rooms)

        course_subjects_button = QPushButton("Asignar materias a cursos")
        course_subjects_button.setMinimumWidth(260)
        course_subjects_button.clicked.connect(self._show_course_subjects)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(school)
        layout.addWidget(teachers_button, alignment=Qt.AlignCenter)
        layout.addWidget(courses_button, alignment=Qt.AlignCenter)
        layout.addWidget(subjects_button, alignment=Qt.AlignCenter)
        layout.addWidget(rooms_button, alignment=Qt.AlignCenter)
        layout.addWidget(course_subjects_button, alignment=Qt.AlignCenter)
        return container

    def _build_status_bar(self) -> None:
        status = QStatusBar()
        status.showMessage("Listo")
        self.setStatusBar(status)

    def _show_home(self) -> None:
        self.tabs.setCurrentIndex(0)

    def _show_teachers(self) -> None:
        self._open_tab("Profesores", TeachersView)

    def _show_courses(self) -> None:
        self._open_tab("Cursos", CoursesView)

    def _show_subjects(self) -> None:
        self._open_tab("Materias", SubjectsView)

    def _show_rooms(self) -> None:
        self._open_tab("Aulas", RoomsView)

    def _show_course_subjects(self) -> None:
        self._open_tab("Materias por curso", CourseSubjectsView)

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
