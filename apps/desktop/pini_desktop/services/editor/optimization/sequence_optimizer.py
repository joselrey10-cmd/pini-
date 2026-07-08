from dataclasses import dataclass

from pini_desktop.services.editor.optimization.chain_builder import ChainBuilder, ChainBuildConfig
from pini_desktop.services.editor.optimization.chain_evaluator import ChainEvaluator, SequenceScore
from pini_desktop.services.editor.optimization.zone_definition import ZoneDefinition
from pini_desktop.services.editor.optimization.zone_optimizer import ZoneOptimizer


@dataclass(frozen=True)
class SequenceOptimizationResult:
    zone: ZoneDefinition
    sequences: tuple[SequenceScore, ...]

    @property
    def best(self) -> SequenceScore | None:
        return self.sequences[0] if self.sequences else None

    @property
    def has_sequences(self) -> bool:
        return bool(self.sequences)


class SequenceOptimizer:
    def __init__(
        self,
        zone_optimizer: ZoneOptimizer | None = None,
        chain_builder: ChainBuilder | None = None,
        evaluator: ChainEvaluator | None = None,
    ):
        self.zone_optimizer = zone_optimizer or ZoneOptimizer()
        self.chain_builder = chain_builder or ChainBuilder()
        self.evaluator = evaluator or ChainEvaluator()

    def optimize(self, zone: ZoneDefinition, max_depth: int = 3, limit: int = 5) -> SequenceOptimizationResult:
        zone_result = self.zone_optimizer.optimize(zone, limit=10)
        chains = self.chain_builder.build(
            zone_result.suggestions,
            ChainBuildConfig(max_depth=max_depth, max_branching=4),
        )
        scores = [self.evaluator.evaluate(chain) for chain in chains]
        scores.sort(key=lambda item: item.score, reverse=True)

        return SequenceOptimizationResult(
            zone=zone,
            sequences=tuple(scores[:limit]),
        )
