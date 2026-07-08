from dataclasses import dataclass

from pini_desktop.services.editor.optimization.predictive_sequence_evaluator import PredictiveSequenceEvaluator
from pini_desktop.services.editor.optimization.predictive_sequence_ranker import PredictiveSequenceRanker
from pini_desktop.services.editor.optimization.sequence_optimizer import SequenceOptimizer
from pini_desktop.services.editor.optimization.zone_definition import ZoneDefinition


@dataclass(frozen=True)
class PredictiveSequenceOptimizationResult:
    zone: ZoneDefinition
    items: tuple[object, ...]

    @property
    def best(self):
        return self.items[0] if self.items else None

    @property
    def has_items(self) -> bool:
        return bool(self.items)


class PredictiveSequenceOptimizer:
    def __init__(
        self,
        sequence_optimizer: SequenceOptimizer | None = None,
        evaluator: PredictiveSequenceEvaluator | None = None,
        ranker: PredictiveSequenceRanker | None = None,
    ):
        self.sequence_optimizer = sequence_optimizer or SequenceOptimizer()
        self.evaluator = evaluator or PredictiveSequenceEvaluator()
        self.ranker = ranker or PredictiveSequenceRanker()

    def optimize(self, zone: ZoneDefinition, max_depth: int = 3, limit: int = 5) -> PredictiveSequenceOptimizationResult:
        result = self.sequence_optimizer.optimize(zone, max_depth=max_depth, limit=limit * 2)
        predictive_items = [self.evaluator.evaluate(item) for item in result.sequences]
        ranked = self.ranker.rank(predictive_items, limit=limit)
        return PredictiveSequenceOptimizationResult(zone=zone, items=ranked)
