import sqlite3
from dataclasses import dataclass
from pini_desktop.config.settings import DATABASE_PATH
from pini_desktop.database.bootstrap import initialise_database

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS dynamic_rules(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    scope TEXT NOT NULL,
    rule_type TEXT NOT NULL,
    priority TEXT NOT NULL,
    target TEXT,
    day INTEGER,
    period INTEGER,
    value TEXT,
    active INTEGER NOT NULL DEFAULT 1,
    notes TEXT
);
"""

@dataclass(frozen=True)
class DynamicRule:
    id: int | None
    code: str
    name: str
    scope: str
    rule_type: str
    priority: str
    target: str = ""
    day: int | None = None
    period: int | None = None
    value: str = ""
    active: bool = True
    notes: str = ""

class DynamicRuleService:
    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        initialise_database()
        self._ensure_table()

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _ensure_table(self) -> None:
        con = self._connect()
        try:
            con.executescript(CREATE_SQL)
            con.commit()
        finally:
            con.close()

    def list_rules(self) -> list[DynamicRule]:
        con = self._connect()
        try:
            rows = con.execute("SELECT * FROM dynamic_rules ORDER BY scope, code").fetchall()
            return [self._row(row) for row in rows]
        finally:
            con.close()

    def create_rule(self, rule: DynamicRule) -> int:
        con = self._connect()
        try:
            cur = con.execute(
                """INSERT INTO dynamic_rules
                (code,name,scope,rule_type,priority,target,day,period,value,active,notes)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (rule.code.strip().upper(), rule.name.strip(), rule.scope, rule.rule_type, rule.priority,
                 rule.target.strip(), rule.day, rule.period, rule.value.strip(), int(rule.active), rule.notes.strip())
            )
            con.commit()
            return int(cur.lastrowid)
        finally:
            con.close()

    def update_rule(self, rule: DynamicRule) -> None:
        if rule.id is None:
            raise ValueError("No se puede actualizar una regla sin id.")
        con = self._connect()
        try:
            con.execute(
                """UPDATE dynamic_rules SET code=?,name=?,scope=?,rule_type=?,priority=?,target=?,
                day=?,period=?,value=?,active=?,notes=? WHERE id=?""",
                (rule.code.strip().upper(), rule.name.strip(), rule.scope, rule.rule_type, rule.priority,
                 rule.target.strip(), rule.day, rule.period, rule.value.strip(), int(rule.active), rule.notes.strip(), rule.id)
            )
            con.commit()
        finally:
            con.close()

    def delete_rule(self, rule_id: int) -> None:
        con = self._connect()
        try:
            con.execute("DELETE FROM dynamic_rules WHERE id=?", (rule_id,))
            con.commit()
        finally:
            con.close()

    def seed_center_rules(self) -> None:
        if self.list_rules():
            return
        base = [
            DynamicRule(None, "R001", "Máximo general 1 consecutiva", "Materia", "Máximo consecutivas", "Obligatoria", "Todas", None, None, "1", True, "Regla general."),
            DynamicRule(None, "R002", "Inglés 4º-6º permite 2 consecutivas", "Materia", "Máximo consecutivas", "Obligatoria", "Inglés 4º-6º", None, None, "2", True, "Excepción."),
            DynamicRule(None, "R003", "Contextos después del recreo", "Materia", "Después del recreo", "Obligatoria", "Contextos", None, None, "Sí", True, "Regla del centro."),
        ]
        for r in base:
            self.create_rule(r)

    def _row(self, row) -> DynamicRule:
        return DynamicRule(
            id=int(row["id"]), code=row["code"], name=row["name"], scope=row["scope"],
            rule_type=row["rule_type"], priority=row["priority"], target=row["target"] or "",
            day=row["day"], period=row["period"], value=row["value"] or "",
            active=bool(row["active"]), notes=row["notes"] or ""
        )
