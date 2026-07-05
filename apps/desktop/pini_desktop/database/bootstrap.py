import sqlite3
from pini_desktop.config.settings import DATA_DIR, DATABASE_PATH

SCHEMA = '''
CREATE TABLE IF NOT EXISTS app_metadata(
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS teachers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    speciality TEXT NOT NULL,
    weekly_hours INTEGER NOT NULL DEFAULT 25,
    max_daily_sessions INTEGER NOT NULL DEFAULT 5
);

CREATE TABLE IF NOT EXISTS courses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    stage TEXT NOT NULL,
    level INTEGER NOT NULL,
    group_name TEXT NOT NULL,
    students INTEGER NOT NULL DEFAULT 25,
    tutor_teacher_id INTEGER,
    FOREIGN KEY(tutor_teacher_id) REFERENCES teachers(id)
);

CREATE TABLE IF NOT EXISTS subjects(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    weekly_sessions INTEGER NOT NULL DEFAULT 1,
    required_speciality TEXT,
    room_type TEXT,
    max_consecutive INTEGER NOT NULL DEFAULT 1,
    allows_double_session INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS rooms(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    room_type TEXT NOT NULL,
    capacity INTEGER NOT NULL DEFAULT 25,
    building TEXT,
    resources TEXT,
    available INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS course_subjects(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    weekly_sessions INTEGER NOT NULL DEFAULT 1,
    preferred_teacher_id INTEGER,
    required_room_type TEXT,
    notes TEXT,
    UNIQUE(course_id, subject_id),
    FOREIGN KEY(course_id) REFERENCES courses(id),
    FOREIGN KEY(subject_id) REFERENCES subjects(id),
    FOREIGN KEY(preferred_teacher_id) REFERENCES teachers(id)
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
