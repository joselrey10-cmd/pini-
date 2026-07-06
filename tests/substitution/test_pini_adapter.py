import sqlite3
from pathlib import Path

from packages.substitution.service import SubstitutionService


def build_db(path: Path):
    con = sqlite3.connect(path)
    con.executescript(
        """
        CREATE TABLE teachers(
            id INTEGER PRIMARY KEY,
            name TEXT,
            surname TEXT,
            speciality TEXT
        );
        CREATE TABLE courses(
            id INTEGER PRIMARY KEY,
            code TEXT
        );
        CREATE TABLE subjects(
            id INTEGER PRIMARY KEY,
            name TEXT,
            required_speciality TEXT
        );
        CREATE TABLE rooms(
            id INTEGER PRIMARY KEY,
            name TEXT
        );
        CREATE TABLE schedule_sessions(
            id INTEGER PRIMARY KEY,
            course_id INTEGER,
            subject_id INTEGER,
            teacher_id INTEGER,
            room_id INTEGER,
            day INTEGER,
            period INTEGER
        );
        CREATE TABLE teacher_availability(
            id INTEGER PRIMARY KEY,
            teacher_id INTEGER,
            day INTEGER,
            period INTEGER,
            status TEXT
        );
        """
    )
    con.execute("INSERT INTO teachers VALUES(1,'Ana','García','Primaria')")
    con.execute("INSERT INTO teachers VALUES(2,'Luis','Pérez','Primaria')")
    con.execute("INSERT INTO teachers VALUES(3,'Marta','López','Música')")
    con.execute("INSERT INTO courses VALUES(1,'1A')")
    con.execute("INSERT INTO subjects VALUES(1,'Lengua','Primaria')")
    con.execute("INSERT INTO rooms VALUES(1,'Aula 1')")
    con.execute("INSERT INTO schedule_sessions VALUES(1,1,1,1,1,1,1)")
    con.execute("INSERT INTO teacher_availability VALUES(1,2,1,1,'PREFERRED')")
    con.commit()
    con.close()


def test_service_reads_candidates_from_pini_db(tmp_path: Path):
    db = tmp_path / "pini.db"
    build_db(db)

    proposals = SubstitutionService(database_path=db).propose_from_pini(1, 1, 1)

    assert proposals
    assert proposals[0].candidate.name == "Luis Pérez"
    assert proposals[0].score >= 90
