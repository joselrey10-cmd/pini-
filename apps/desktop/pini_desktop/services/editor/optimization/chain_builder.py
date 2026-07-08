from dataclasses import dataclass

from pini_desktop.services.editor.optimization.move_sequence import MoveSequence, MoveStep
from pini_desktop.services.editor.optimization.zone_optimizer import ZoneOptimizationSuggestion


@dataclass(frozen=True)
class ChainBuildConfig:
    max_depth: int = 3
    max_branching: int = 3


class ChainBuilder:
    """Construye cadenas de movimientos a partir de sugerencias individuales.

    Esta primera versión evita repetir la misma sesión dentro de una cadena.
    """

    def build(
        self,
        suggestions: tuple[ZoneOptimizationSuggestion, ...] | list[ZoneOptimizationSuggestion],
        config: ChainBuildConfig | None = None,
    ) -> tuple[MoveSequence, ...]:
        config = config or ChainBuildConfig()
        base = list(suggestions)[: max(1, config.max_branching)]
        chains = []

        def expand(current: MoveSequence, remaining: list[ZoneOptimizationSuggestion]):
            if current.length >= config.max_depth or not remaining:
                if current.length > 0:
                    chains.append(current)
                return

            for suggestion in remaining[: config.max_branching]:
                if suggestion.session_id in current.session_ids:
                    continue

                step = MoveStep(
                    order=current.length + 1,
                    session_id=suggestion.session_id,
                    day=suggestion.day,
                    period=suggestion.period,
                    estimated_delta=suggestion.estimated_delta,
                    title=suggestion.title,
                )
                next_sequence = current.append(step)
                next_remaining = [item for item in remaining if item.session_id != suggestion.session_id]
                expand(next_sequence, next_remaining)

        expand(MoveSequence(steps=()), base)
        chains.sort(key=lambda chain: (chain.estimated_delta, chain.length), reverse=True)
        return tuple(chains)
