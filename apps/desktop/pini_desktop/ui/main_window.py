from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QMessageBox, QPushButton, QStatusBar, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Pini 0.1 - Planificador Inteligente")
        self.resize(1100, 720)
        self._build_menu()
        self._build_central_widget()
        self._build_status_bar()

    def _build_menu(self) -> None:
        menu = self.menuBar()

        file_menu = menu.addMenu("Archivo")
        file_menu.addAction("Nuevo proyecto", self._not_implemented)
        file_menu.addAction("Abrir proyecto", self._not_implemented)
        file_menu.addAction("Guardar", self._not_implemented)
        file_menu.addSeparator()
        file_menu.addAction("Salir", self.close)

        center_menu = menu.addMenu("Centro")
        center_menu.addAction("Configuración", self._not_implemented)
        center_menu.addAction("Calendario", self._not_implemented)
        center_menu.addAction("Horario general", self._not_implemented)

        data_menu = menu.addMenu("Datos")
        data_menu.addAction("Profesores", self._not_implemented)
        data_menu.addAction("Cursos", self._not_implemented)
        data_menu.addAction("Materias", self._not_implemented)
        data_menu.addAction("Aulas", self._not_implemented)

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

        new_project = QPushButton("Nuevo proyecto")
        new_project.setMinimumWidth(260)
        new_project.clicked.connect(self._not_implemented)

        open_project = QPushButton("Abrir proyecto")
        open_project.setMinimumWidth(260)
        open_project.clicked.connect(self._not_implemented)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(school)
        layout.addWidget(new_project, alignment=Qt.AlignCenter)
        layout.addWidget(open_project, alignment=Qt.AlignCenter)
        self.setCentralWidget(container)

    def _build_status_bar(self) -> None:
        status = QStatusBar()
        status.showMessage("Listo")
        self.setStatusBar(status)

    def _about(self) -> None:
        QMessageBox.information(self, "Acerca de Pini", "Pini 0.1\nPlanificador Inteligente de Horarios Escolares.")

    def _not_implemented(self) -> None:
        QMessageBox.information(self, "Pini", "Esta función se implementará en los próximos commits.")
