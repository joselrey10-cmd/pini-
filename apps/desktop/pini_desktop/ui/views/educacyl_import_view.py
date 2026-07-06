from PySide6.QtWidgets import (
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from pini_desktop.services.educacyl_service import DesktopEducaCyLService


class EducaCyLImportView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = DesktopEducaCyLService()

        title = QLabel("Importación EducaCyL")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        description = QLabel(
            "Asistente inicial de integración. En esta fase usa un cliente simulado y una caché local. "
            "No conecta con servicios privados ni solicita credenciales reales."
        )
        description.setWordWrap(True)

        self.username_input = QLineEdit("demo")
        self.token_input = QLineEdit("mock-token")

        form = QFormLayout()
        form.addRow("Usuario / identificador", self.username_input)
        form.addRow("Token simulado", self.token_input)

        sync_button = QPushButton("Sincronizar datos simulados")
        sync_button.clicked.connect(self.sync_mock)

        cache_button = QPushButton("Ver última sincronización")
        cache_button.clicked.connect(self.show_cache)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addLayout(form)
        layout.addWidget(sync_button)
        layout.addWidget(cache_button)
        layout.addWidget(self.output)

    def sync_mock(self) -> None:
        summary = self.service.sync_mock(
            username=self.username_input.text().strip() or "demo",
            token=self.token_input.text().strip() or "mock",
        )

        text = [
            "Sincronización completada",
            f"Autenticado: {'Sí' if summary.authenticated else 'No'}",
            f"Origen: {summary.source}",
            f"Profesores: {summary.teachers}",
            f"Cursos: {summary.courses}",
            f"Materias: {summary.subjects}",
            f"Aulas: {summary.rooms}",
            f"Última sincronización: {summary.last_sync}",
        ]

        if summary.warnings:
            text.append("")
            text.append("Avisos:")
            text.extend(f"- {warning}" for warning in summary.warnings)

        self.output.setPlainText("\n".join(text))
        QMessageBox.information(self, "EducaCyL", "Sincronización simulada completada.")

    def show_cache(self) -> None:
        metadata = self.service.cache_metadata()
        if not metadata:
            self.output.setPlainText("Todavía no hay sincronizaciones registradas.")
            return

        self.output.setPlainText(
            "\n".join(
                [
                    "Última sincronización",
                    f"Origen: {metadata.get('source', '')}",
                    f"Fecha: {metadata.get('last_sync', '')}",
                ]
            )
        )
