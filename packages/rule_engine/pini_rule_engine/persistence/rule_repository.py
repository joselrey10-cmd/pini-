import sqlite3
from pini_rule_engine.domain.exception import RuleException
from pini_rule_engine.domain.parameter import RuleParameter
from pini_rule_engine.domain.rule import Rule, RuleType

class RuleRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def clear_all(self) -> None:
        self.connection.execute("DELETE FROM rule_exceptions")
        self.connection.execute("DELETE FROM rule_parameters")
        self.connection.execute("DELETE FROM rules")
        self.connection.commit()

    def save_rule(self, rule: Rule) -> None:
        self.connection.execute(
            "INSERT OR REPLACE INTO rules(code,name,category,type,enabled,weight,description) VALUES(?,?,?,?,?,?,?)",
            (rule.code, rule.name, rule.category, rule.rule_type.value, int(rule.enabled), rule.weight, rule.description),
        )
        self.connection.commit()

    def get_rule(self, code: str) -> Rule | None:
        row = self.connection.execute("SELECT * FROM rules WHERE code=?", (code,)).fetchone()
        if row is None:
            return None
        return Rule(row["code"], row["name"], row["category"], RuleType(row["type"]), bool(row["enabled"]), int(row["weight"]), row["description"] or "")

    def list_rules(self) -> list[Rule]:
        rows = self.connection.execute("SELECT * FROM rules ORDER BY code").fetchall()
        return [Rule(row["code"], row["name"], row["category"], RuleType(row["type"]), bool(row["enabled"]), int(row["weight"]), row["description"] or "") for row in rows]

    def save_parameter(self, parameter: RuleParameter) -> None:
        self.connection.execute(
            "INSERT OR REPLACE INTO rule_parameters(rule_code,key,value) VALUES(?,?,?)",
            (parameter.rule_code, parameter.key, parameter.value),
        )
        self.connection.commit()

    def get_parameter(self, rule_code: str, key: str, default: str | None = None) -> str | None:
        row = self.connection.execute(
            "SELECT value FROM rule_parameters WHERE rule_code=? AND key=?",
            (rule_code, key),
        ).fetchone()
        return row["value"] if row else default

    def save_exception(self, exception: RuleException) -> None:
        self.connection.execute(
            "INSERT INTO rule_exceptions(rule_code,subject,course_from,course_to,parameter,value) VALUES(?,?,?,?,?,?)",
            (exception.rule_code, exception.subject, exception.course_from, exception.course_to, exception.parameter, exception.value),
        )
        self.connection.commit()

    def list_exceptions(self, rule_code: str) -> list[RuleException]:
        rows = self.connection.execute(
            "SELECT rule_code,subject,course_from,course_to,parameter,value FROM rule_exceptions WHERE rule_code=?",
            (rule_code,),
        ).fetchall()
        return [RuleException(row["rule_code"], row["subject"], int(row["course_from"]), int(row["course_to"]), row["parameter"], row["value"]) for row in rows]
