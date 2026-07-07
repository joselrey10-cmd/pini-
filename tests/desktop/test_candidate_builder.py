from pini_desktop.services.editor.optimization.candidate_builder import CandidateBuilder


def test_candidate_builder_generates_nearby_candidates():
    candidates = CandidateBuilder().build_move_candidates(
        session_id=1,
        current_day=2,
        current_period=3,
        radius=1,
    )

    assert candidates
    assert all(candidate.session_id == 1 for candidate in candidates)
    assert all(not (candidate.day == 2 and candidate.period == 3) for candidate in candidates)


def test_candidate_builder_generates_day_candidates():
    candidates = CandidateBuilder().build_day_candidates(
        session_id=1,
        current_day=2,
        current_period=3,
    )

    assert len(candidates) == 4
    assert all(candidate.period == 3 for candidate in candidates)


def test_alternative_generator_returns_limited_alternatives():
    from pini_desktop.services.editor.optimization.alternative_generator import AlternativeGenerator

    alternatives = AlternativeGenerator().generate_for_session(1, 2, 3, limit=3)

    assert len(alternatives) <= 3
    assert alternatives[0].estimated_delta > 0


def test_alternatives_panel_can_be_imported():
    from pini_desktop.ui.views.alternatives_panel import AlternativesPanel

    assert AlternativesPanel is not None
