from packages.optimizer.explainer import OptimizationExplainer
from packages.optimizer.explanation_report import OptimizationExplanationReport
from packages.optimizer.models import Session
from packages.optimizer.solution import Solution


def test_explainer_returns_summary_and_items():
    before = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Ana", "2A", "Mate", "A2", 1, 1),
        ]
    )

    after = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
            Session("Luis", "2A", "Mate", "A2", 1, 2),
        ]
    )

    explanation = OptimizationExplainer().explain(before, after)

    assert explanation.summary
    assert explanation.items
    assert isinstance(explanation.improvement, float)


def test_explanation_report_has_expected_fields():
    solution = Solution(
        sessions=[
            Session("Ana", "1A", "Lengua", "A1", 1, 1),
        ]
    )

    report = OptimizationExplanationReport().build(solution, solution)

    assert "summary" in report
    assert "items" in report
    assert report["before_score"] == report["after_score"]
