import sqlite3
from pathlib import Path

from pini_desktop.services.editor.optimization.zone_candidate_provider import ZoneCandidateProvider
from pini_desktop.services.editor.optimization.zone_definition import ZoneDefinition
from pini_desktop.services.editor.optimization.zone_optimizer import ZoneOptimizer
from pini_desktop.services.editor.optimization.zone_report import ZoneOptimizationReport
from pini_desktop.services.editor.optimization.zone_score import ZoneScoreCalculator

def setup_db(path: Path):
    con = sqlite3.connect(path)
    con.executescript("""
        CREATE TABLE schedule_sessions(
            id INTEGER PRIMARY KEY,
            course_id INTEGER,
            subject_id INTEGER,
            teacher_id INTEGER,
            room_id INTEGER,
            day INTEGER,
            period INTEGER
        );
        INSERT INTO schedule_sessions VALUES(1,1,1,10,1,1,1);
        INSERT INTO schedule_sessions VALUES(2,1,1,10,1,1,3);
        INSERT INTO schedule_sessions VALUES(3,2,1,20,1,2,6);
    """)
    con.commit()
    con.close()

def test_zone_provider_filters_teacher(tmp_path: Path):
    db = tmp_path / "pini.db"
    setup_db(db)
    sessions = ZoneCandidateProvider(database_path=db).list_sessions(ZoneDefinition("teacher", entity_id=10))
    assert len(sessions) == 2

def test_zone_score_counts_gaps():
    class S:
        def __init__(self, day, period):
            self.day = day
            self.period = period
    score = ZoneScoreCalculator().calculate([S(1, 1), S(1, 3), S(2, 6)])
    assert score.gaps == 1
    assert score.last_periods == 1
    assert score.score < 100

def test_zone_optimizer_returns_suggestions(tmp_path: Path):
    db = tmp_path / "pini.db"
    setup_db(db)
    optimizer = ZoneOptimizer(provider=ZoneCandidateProvider(database_path=db))
    result = optimizer.optimize(ZoneDefinition("teacher", entity_id=10), limit=3)
    assert result.before.sessions == 2
    assert len(result.suggestions) <= 3
    assert "score" in ZoneOptimizationReport().build(result)

def test_zone_optimization_panel_import():
    from pini_desktop.ui.views.zone_optimization_panel import ZoneOptimizationPanel
    assert ZoneOptimizationPanel is not None
