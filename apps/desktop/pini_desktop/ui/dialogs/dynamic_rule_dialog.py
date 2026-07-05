from PySide6.QtWidgets import QCheckBox, QComboBox, QDialog, QFormLayout, QHBoxLayout, QLineEdit, QMessageBox, QPushButton, QSpinBox, QTextEdit, QVBoxLayout
from pini_desktop.services.dynamic_rule_service import DynamicRule

SCOPES = ["Profesorado", "Curso", "Materia", "Aula", "Centro"]
TYPES = ["No permitir franja", "Preferir franja", "Evitar franja", "Máximo diario", "Máximo consecutivas", "Después del recreo", "Aula obligatoria", "Nota personalizada"]
PRIORITIES = ["Obligatoria", "Preferente", "Deseable"]

class DynamicRuleDialog(QDialog):
    def __init__(self, parent=None, rule: DynamicRule | None = None):
        super().__init__(parent)
        self.setWindowTitle("Regla del centro")
        self.rule = rule
        self.code_input = QLineEdit()
        self.name_input = QLineEdit()
        self.scope_input = QComboBox(); self.scope_input.addItems(SCOPES)
        self.type_input = QComboBox(); self.type_input.addItems(TYPES)
        self.priority_input = QComboBox(); self.priority_input.addItems(PRIORITIES)
        self.target_input = QLineEdit()
        self.day_input = QSpinBox(); self.day_input.setRange(0,5); self.day_input.setSpecialValueText("Cualquiera")
        self.period_input = QSpinBox(); self.period_input.setRange(0,8); self.period_input.setSpecialValueText("Cualquiera")
        self.value_input = QLineEdit()
        self.active_input = QCheckBox("Regla activa"); self.active_input.setChecked(True)
        self.notes_input = QTextEdit(); self.notes_input.setFixedHeight(70)

        if rule:
            self.code_input.setText(rule.code); self.name_input.setText(rule.name)
            self._select(self.scope_input, rule.scope); self._select(self.type_input, rule.rule_type); self._select(self.priority_input, rule.priority)
            self.target_input.setText(rule.target); self.day_input.setValue(rule.day or 0); self.period_input.setValue(rule.period or 0)
            self.value_input.setText(rule.value); self.active_input.setChecked(rule.active); self.notes_input.setPlainText(rule.notes)

        form = QFormLayout()
        form.addRow("Código", self.code_input); form.addRow("Nombre", self.name_input)
        form.addRow("Ámbito", self.scope_input); form.addRow("Tipo", self.type_input); form.addRow("Prioridad", self.priority_input)
        form.addRow("Afecta a", self.target_input); form.addRow("Día", self.day_input); form.addRow("Periodo", self.period_input)
        form.addRow("Valor", self.value_input); form.addRow("", self.active_input); form.addRow("Notas", self.notes_input)

        save = QPushButton("Guardar"); save.clicked.connect(self._accept_if_valid)
        cancel = QPushButton("Cancelar"); cancel.clicked.connect(self.reject)
        buttons = QHBoxLayout(); buttons.addStretch(); buttons.addWidget(save); buttons.addWidget(cancel)
        layout = QVBoxLayout(self); layout.addLayout(form); layout.addLayout(buttons)

    def get_rule(self) -> DynamicRule:
        return DynamicRule(
            id=self.rule.id if self.rule else None,
            code=self.code_input.text().strip().upper(),
            name=self.name_input.text().strip(),
            scope=self.scope_input.currentText(),
            rule_type=self.type_input.currentText(),
            priority=self.priority_input.currentText(),
            target=self.target_input.text().strip(),
            day=self.day_input.value() or None,
            period=self.period_input.value() or None,
            value=self.value_input.text().strip(),
            active=self.active_input.isChecked(),
            notes=self.notes_input.toPlainText().strip(),
        )

    def _accept_if_valid(self):
        r = self.get_rule()
        if not r.code or not r.name:
            QMessageBox.warning(self, "Datos incompletos", "Rellena código y nombre.")
            return
        self.accept()

    def _select(self, combo, text):
        idx = combo.findText(text)
        if idx >= 0:
            combo.setCurrentIndex(idx)
