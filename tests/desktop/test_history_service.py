from pini_desktop.services.editor.optimization.history_service import (
    HistoryService,
)


def test_history_adds_entries():
    history = HistoryService()

    history.add("Mover Matemáticas", 2.5)
    history.add("Mover Inglés", 1.0)

    entries = history.entries()

    assert len(entries) == 2
    assert entries[0].description == "Mover Matemáticas"
    assert entries[1].score_delta == 1.0


def test_history_can_be_cleared():
    history = HistoryService()

    history.add("Cambio", 0.5)

    history.clear()

    assert history.entries() == ()