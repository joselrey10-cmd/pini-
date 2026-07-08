from dataclasses import dataclass

from pini_desktop.services.editor.optimization.future_simulation import FutureSimulationEngine


@dataclass(frozen=True)
class PredictiveSequenceScore:
    sequence_score: object
    simulation: object
    predictive_score: float
    recommendation: str


class PredictiveSequenceEvaluator:
    def __init__(self, simulation_engine: FutureSimulationEngine | None = None):
        self.simulation_engine = simulation_engine or FutureSimulationEngine()

    def evaluate(self, sequence_score) -> PredictiveSequenceScore:
        simulation = self.simulation_engine.simulate_sequence(sequence_score.sequence)
        predictive_score = round(sequence_score.score + simulation.impact.future_delta, 2)

        if simulation.is_recommended and predictive_score > 0:
            recommendation = "Cadena recomendable también a futuro."
        elif predictive_score > 0:
            recommendation = "Cadena positiva, pero revisar riesgos futuros."
        else:
            recommendation = "No recomendada por impacto futuro."

        return PredictiveSequenceScore(
            sequence_score=sequence_score,
            simulation=simulation,
            predictive_score=predictive_score,
            recommendation=recommendation,
        )
