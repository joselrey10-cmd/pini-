from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QLabel, QListWidget, QMessageBox, QPushButton, QVBoxLayout, QWidget

from pini_desktop.services.backup_service import BackupService


class BackupView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = BackupService()

        title = QLabel("Copias de seguridad")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.list_widget = QListWidget()

        create_auto_button = QPushButton("Crear copia automática")
        create_auto_button.clicked.connect(self.create_auto_backup)

        create_as_button = QPushButton("Guardar copia como...")
        create_as_button.clicked.connect(self.create_backup_as)

        restore_file_button = QPushButton("Restaurar desde archivo...")
        restore_file_button.clicked.connect(self.restore_from_file)

        refresh_button = QPushButton("Actualizar lista")
        refresh_button.clicked.connect(self.load_backups)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.list_widget)
        layout.addWidget(create_auto_button)
        layout.addWidget(create_as_button)
        layout.addWidget(restore_file_button)
        layout.addWidget(refresh_button)
        layout.addStretch()

        self.load_backups()

    def load_backups(self) -> None:
        self.list_widget.clear()
        for path in self.service.list_backups():
            self.list_widget.addItem(str(path))

    def create_auto_backup(self) -> None:
        self._show_result(self.service.create_backup())
        self.load_backups()

    def create_backup_as(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Guardar copia", str(Path.home() / "pini_backup.db"), "SQLite DB (*.db)")
        if path:
            self._show_result(self.service.create_backup(path))
            self.load_backups()

    def restore_from_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Seleccionar copia", str(Path.home()), "SQLite DB (*.db)")
        if not path:
            return
        confirm = QMessageBox.question(self, "Restaurar copia", "Esto sustituirá los datos actuales. ¿Continuar?")
        if confirm == QMessageBox.Yes:
            self._show_result(self.service.restore_backup(path))
            self.load_backups()

    def _show_result(self, result) -> None:
        if result.created:
            QMessageBox.information(self, "Copias de seguridad", f"{result.message}\\n{result.path}")
        else:
            QMessageBox.warning(self, "Copias de seguridad", result.message)
