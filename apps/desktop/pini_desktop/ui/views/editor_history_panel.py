from PySide6.QtWidgets import QLabel, QListWidget, QPushButton, QVBoxLayout, QWidget


class EditorHistoryPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        title = QLabel("Historial del editor")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.list_widget = QListWidget()

        self.clear_button = QPushButton("Limpiar vista")
        self.clear_button.clicked.connect(self.clear)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.clear_button)

    def add_result(self, action: str, result) -> None:
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

    def clear(self) -> None:
        self.list_widget.clear()
