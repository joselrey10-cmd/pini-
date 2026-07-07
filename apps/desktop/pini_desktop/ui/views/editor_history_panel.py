from PySide6.QtWidgets import QLabel, QListWidget, QPushButton, QVBoxLayout, QWidget

from pini_desktop.services.editor.history.editor_history_service import EditorHistoryService


class EditorHistoryPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.history_service = EditorHistoryService()

        title = QLabel("Historial del editor")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.list_widget = QListWidget()

        reload_button = QPushButton("Cargar historial guardado")
        reload_button.clicked.connect(self.load_persistent_history)

        clear_view_button = QPushButton("Limpiar vista")
        clear_view_button.clicked.connect(self.clear_view)

        clear_db_button = QPushButton("Borrar historial guardado")
        clear_db_button.clicked.connect(self.clear_persistent_history)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.list_widget)
        layout.addWidget(reload_button)
        layout.addWidget(clear_view_button)
        layout.addWidget(clear_db_button)

    def add_result(self, action: str, result) -> None:
        self.history_service.record_result(action, result)
        status = "✓" if getattr(result, "success", False) else "✗"
        messages = getattr(result, "messages", ()) or ()
        warnings = getattr(result, "warnings", ()) or ()

        main_message = ""
        if messages:
            main_message = str(messages[0])
        elif warnings:
            main_message = str(warnings[0])

        self.list_widget.insertItem(0, f"{status} {action}: {main_message}".strip())

    def add_text(self, text: str) -> None:
        self.list_widget.insertItem(0, text)

    def load_persistent_history(self) -> None:
        self.list_widget.clear()
        for record in self.history_service.list_records():
            status = "✓" if record.success else "✗"
            score = ""
            if record.old_score is not None and record.new_score is not None:
                score = f" ({record.old_score} → {record.new_score})"
            message = record.messages.splitlines()[0] if record.messages else ""
            self.list_widget.addItem(f"{status} {record.created_at} · {record.action}{score} · {message}")

    def clear_view(self) -> None:
        self.list_widget.clear()

    def clear_persistent_history(self) -> None:
        self.history_service.clear()
        self.list_widget.clear()
