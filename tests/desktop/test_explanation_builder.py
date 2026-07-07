from pini_desktop.services.editor.optimization.candidate_builder import MoveCandidate
from pini_desktop.services.editor.optimization.explanation_builder import ExplanationBuilder
from pini_desktop.services.editor.optimization.score_estimator import EstimatedScore


def test_explanation_builder_creates_summary_and_bullets():
    candidate = MoveCandidate(1, 2, 3, "Mover")
    estimated = EstimatedScore(
        candidate=candidate,
        current_score=80,
        estimated_score=82,
        delta=2,
        reasons=("Mejora el reparto entre días.",),
    )

    explanation = ExplanationBuilder().build(estimated)

    assert "recomendable" in explanation.summary.lower()
    assert explanation.bullets
    assert explanation.bullets[0].startswith("✔")


def test_alternative_generator_adds_explanations():
    from pini_desktop.services.editor.optimization.alternative_generator import AlternativeGenerator

    alternatives = AlternativeGenerator().generate_for_session(1, 2, 3, limit=2)

    assert alternatives
    assert alternatives[0].explanation
    assert alternatives[0].bullets
