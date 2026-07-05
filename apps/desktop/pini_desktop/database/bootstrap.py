import sqlite3
from pini_desktop.config.settings import DATA_DIR, DATABASE_PATH

SCHEMA = '''
CREATE TABLE IF NOT EXISTS app_metadata(
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
'''

def initialise_database() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        connection.executescript(SCHEMA)
        connection.execute(
            "INSERT OR REPLACE INTO app_metadata(key, value) VALUES(?, ?)",
            ("version", "0.1.0"),
        )
        connection.commit()
    finally:
        connection.close()
