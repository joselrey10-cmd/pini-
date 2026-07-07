from PySide6.QtCore import QMimeData, Qt, Signal
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import QAbstractItemView, QTableWidget


class ScheduleDragDropTable(QTableWidget):
    """Tabla de horario con Drag & Drop interno.

    Emite:
    - sessionMoved(session_id, target_day, target_period)
    - sessionsSwapped(source_session_id, target_session_id)
    """

    sessionMoved = Signal(int, int, int)
    sessionsSwapped = Signal(int, int)

    SESSION_ID_ROLE = Qt.UserRole
    DAY_ROLE = Qt.UserRole + 1
    PERIOD_ROLE = Qt.UserRole + 2
    MIME_TYPE = "application/x-pini-schedule-session"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

    def startDrag(self, supported_actions):
        item = self.currentItem()
        if item is None:
            return

        session_id = item.data(self.SESSION_ID_ROLE)
        if session_id is None:
            return

        mime = QMimeData()
        mime.setData(self.MIME_TYPE, str(session_id).encode("utf-8"))

        drag = QDrag(self)
        drag.setMimeData(mime)
        drag.exec(Qt.MoveAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(self.MIME_TYPE):
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat(self.MIME_TYPE):
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if not event.mimeData().hasFormat(self.MIME_TYPE):
            super().dropEvent(event)
            return

        item = self.itemAt(event.position().toPoint())
        if item is None:
            event.ignore()
            return

        source_session_id = int(bytes(event.mimeData().data(self.MIME_TYPE)).decode("utf-8"))
        target_session_id = item.data(self.SESSION_ID_ROLE)
        target_day = item.data(self.DAY_ROLE)
        target_period = item.data(self.PERIOD_ROLE)

        if target_session_id is None:
            self.sessionMoved.emit(source_session_id, int(target_day), int(target_period))
        elif int(target_session_id) != source_session_id:
            self.sessionsSwapped.emit(source_session_id, int(target_session_id))

        event.acceptProposedAction()
