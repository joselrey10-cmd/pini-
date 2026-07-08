from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from pini_desktop.services.editor.history.schedule_version_comparator import ScheduleVersionComparator
from pini_desktop.services.editor.history.schedule_version_service import ScheduleVersionService


class ScheduleVersionComparePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.version_service = ScheduleVersionService()
        self.comparator = ScheduleVersionComparator()

        title = QLabel("Comparar versiones")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.first_combo = QComboBox()
        self.second_combo = QComboBox()

        compare_button = QPushButton("Comparar")
        compare_button.clicked.connect(self.compare_versions)

        refresh_button = QPushButton("Actualizar versiones")
        refresh_button.clicked.connect(self.load_versions)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(QLabel("Versión A"))
        layout.addWidget(self.first_combo)
        layout.addWidget(QLabel("Versión B"))
        layout.addWidget(self.second_combo)
        layout.addWidget(compare_button)
        layout.addWidget(refresh_button)
        layout.addWidget(self.output)

        self.load_versions()

    def load_versions(self):
        versions = self.version_service.list_versions()
        self.first_combo.clear()
        self.second_combo.clear()

        for version in versions:
            label = f"{version.id} · {version.name} · {version.created_at}"
            self.first_combo.addItem(label, version.id)
            self.second_combo.addItem(label, version.id)

        if self.second_combo.count() > 1:
            self.second_combo.setCurrentIndex(1)

    def compare_versions(self):
        first_id = self.first_combo.currentData()
        second_id = self.second_combo.currentData()

        if first_id is None or second_id is None:
            QMessageBox.information(self, "Comparar versiones", "Necesitas al menos dos versiones.")
            return

        if first_id == second_id:
            QMessageBox.information(self, "Comparar versiones", "Selecciona dos versiones diferentes.")
            return

        comparison = self.comparator.compare(int(first_id), int(second_id))

        self.output.setPlainText(
            "\n".join(
                [
                    comparison.summary,
                    "",
                    f"Sesiones versión A: {comparison.first_sessions}",
                    f"Sesiones versión B: {comparison.second_sessions}",
                    f"Sesiones añadidas: {comparison.added}",
                    f"Sesiones eliminadas: {comparison.removed}",
                    f"Sesiones movidas: {comparison.moved}",
                ]
            )
        )
