from PySide6.QtWidgets import (
    QInputDialog,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from pini_desktop.services.editor.history.schedule_version_service import ScheduleVersionService


class ScheduleVersionsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = ScheduleVersionService()

        title = QLabel("Versiones del horario")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.list_widget = QListWidget()

        create_button = QPushButton("Crear versión")
        create_button.clicked.connect(self.create_version)

        restore_button = QPushButton("Restaurar versión")
        restore_button.clicked.connect(self.restore_selected)

        delete_button = QPushButton("Eliminar versión")
        delete_button.clicked.connect(self.delete_selected)

        refresh_button = QPushButton("Actualizar")
        refresh_button.clicked.connect(self.load_versions)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.list_widget)
        layout.addWidget(create_button)
        layout.addWidget(restore_button)
        layout.addWidget(delete_button)
        layout.addWidget(refresh_button)

        self.load_versions()

    def load_versions(self):
        self.list_widget.clear()
        for version in self.service.list_versions():
            self.list_widget.addItem(
                f"{version.id} · {version.created_at} · {version.name} · {version.sessions_count} sesiones"
            )

    def selected_version_id(self):
        item = self.list_widget.currentItem()
        if item is None:
            QMessageBox.information(self, "Versión", "Selecciona una versión.")
            return None
        return int(item.text().split("·", 1)[0].strip())

    def create_version(self):
        name, ok = QInputDialog.getText(self, "Crear versión", "Nombre de la versión:")
        if not ok:
            return
        description, _ = QInputDialog.getText(self, "Crear versión", "Descripción:")
        self.service.create_version(name, description)
        self.load_versions()

    def restore_selected(self):
        version_id = self.selected_version_id()
        if version_id is None:
            return

        answer = QMessageBox.question(
            self,
            "Restaurar versión",
            "Esto sustituirá el horario actual por la versión seleccionada. ¿Continuar?",
        )
        if answer != QMessageBox.Yes:
            return

        self.service.restore_version(version_id)
        QMessageBox.information(self, "Versión restaurada", "Horario restaurado correctamente.")
        self.load_versions()

    def delete_selected(self):
        version_id = self.selected_version_id()
        if version_id is None:
            return
        self.service.delete_version(version_id)
        self.load_versions()
