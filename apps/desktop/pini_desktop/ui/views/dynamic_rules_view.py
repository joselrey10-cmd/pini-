import sqlite3
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from pini_desktop.services.dynamic_rule_service import DynamicRuleService, DynamicRule
from pini_desktop.ui.dialogs.dynamic_rule_dialog import DynamicRuleDialog

class DynamicRulesView(QWidget):
    HEADERS = ["ID", "Código", "Nombre", "Ámbito", "Tipo", "Prioridad", "Afecta a", "Día", "Periodo", "Valor", "Activa"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = DynamicRuleService()
        self.table = QTableWidget(); self.table.setColumnCount(len(self.HEADERS)); self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.setSelectionBehavior(QTableWidget.SelectRows); self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_rule)
        add = QPushButton("Añadir regla"); add.clicked.connect(self.add_rule)
        edit = QPushButton("Editar"); edit.clicked.connect(self.edit_rule)
        delete = QPushButton("Eliminar"); delete.clicked.connect(self.delete_rule)
        seed = QPushButton("Cargar reglas base"); seed.clicked.connect(self.seed_rules)
        refresh = QPushButton("Actualizar"); refresh.clicked.connect(self.load_rules)
        buttons = QHBoxLayout()
        for b in [add, edit, delete, seed]: buttons.addWidget(b)
        buttons.addStretch(); buttons.addWidget(refresh)
        layout = QVBoxLayout(self); layout.addLayout(buttons); layout.addWidget(self.table)
        self.load_rules()

    def load_rules(self):
        rules = self.service.list_rules()
        self.table.setRowCount(len(rules))
        for r, rule in enumerate(rules):
            vals = [rule.id, rule.code, rule.name, rule.scope, rule.rule_type, rule.priority, rule.target, rule.day or "", rule.period or "", rule.value, "Sí" if rule.active else "No"]
            for c, v in enumerate(vals):
                item = QTableWidgetItem(str(v))
                if c == 0: item.setData(Qt.UserRole, rule)
                self.table.setItem(r, c, item)
        self.table.resizeColumnsToContents()

    def add_rule(self):
        d = DynamicRuleDialog(self)
        if d.exec():
            try:
                self.service.create_rule(d.get_rule()); self.load_rules()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Código duplicado", "Ya existe una regla con ese código.")

    def edit_rule(self):
        rule = self._selected()
        if not rule:
            QMessageBox.information(self, "Selecciona regla", "Selecciona una regla.")
            return
        d = DynamicRuleDialog(self, rule)
        if d.exec():
            try:
                self.service.update_rule(d.get_rule()); self.load_rules()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Código duplicado", "Ya existe una regla con ese código.")

    def delete_rule(self):
        rule = self._selected()
        if not rule:
            QMessageBox.information(self, "Selecciona regla", "Selecciona una regla.")
            return
        if QMessageBox.question(self, "Eliminar regla", f"¿Eliminar {rule.code}?") == QMessageBox.Yes:
            self.service.delete_rule(rule.id); self.load_rules()

    def seed_rules(self):
        self.service.seed_center_rules(); self.load_rules()

    def _selected(self) -> DynamicRule | None:
        rows = self.table.selectionModel().selectedRows()
        if not rows: return None
        return self.table.item(rows[0].row(), 0).data(Qt.UserRole)
