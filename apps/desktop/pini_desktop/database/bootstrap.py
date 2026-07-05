import sqlite3
from pini_desktop.config.settings import DATA_DIR, DATABASE_PATH

SCHEMA = """
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

CREATE TABLE IF NOT EXISTS teacher_availability(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    day INTEGER NOT NULL,
    period INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'AVAILABLE',
    UNIQUE(teacher_id, day, period),
    FOREIGN KEY(teacher_id) REFERENCES teachers(id)
);

CREATE TABLE IF NOT EXISTS timetable_settings(
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS timetable_periods(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day INTEGER NOT NULL,
    period INTEGER NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    is_break_after INTEGER NOT NULL DEFAULT 0,
    is_after_break INTEGER NOT NULL DEFAULT 0,
    UNIQUE(day, period)
);

CREATE TABLE IF NOT EXISTS schedule_sessions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    teacher_id INTEGER,
    room_id INTEGER,
    day INTEGER NOT NULL,
    period INTEGER NOT NULL,
    locked INTEGER NOT NULL DEFAULT 0,
    generated_by TEXT NOT NULL DEFAULT 'basic',
    FOREIGN KEY(course_id) REFERENCES courses(id),
    FOREIGN KEY(subject_id) REFERENCES subjects(id),
    FOREIGN KEY(teacher_id) REFERENCES teachers(id),
    FOREIGN KEY(room_id) REFERENCES rooms(id)
);

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
