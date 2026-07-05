import sys
from PySide6.QtWidgets import QApplication
from pini_desktop.database.bootstrap import initialise_database
from pini_desktop.ui.main_window import MainWindow

def main() -> int:
    initialise_database()
    app = QApplication(sys.argv)
    app.setApplicationName("Pini")
    app.setOrganizationName("CEIP Tierra de Pinares")
    window = MainWindow()
    window.show()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())
