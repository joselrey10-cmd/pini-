CREATE TABLE IF NOT EXISTS rules(
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    type TEXT NOT NULL,
    enabled INTEGER NOT NULL,
    weight INTEGER NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS rule_parameters(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_code TEXT NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    UNIQUE(rule_code, key)
);

CREATE TABLE IF NOT EXISTS rule_exceptions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_code TEXT NOT NULL,
    subject TEXT NOT NULL,
    course_from INTEGER NOT NULL,
    course_to INTEGER NOT NULL,
    parameter TEXT NOT NULL,
    value TEXT NOT NULL
);
