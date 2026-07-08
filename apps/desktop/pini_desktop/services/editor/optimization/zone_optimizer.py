from dataclasses import dataclass

from pini_desktop.services.editor.optimization.candidate_builder import CandidateBuilder
from pini_desktop.services.editor.optimization.score_estimator import ScoreEstimator
from pini_desktop.services.editor.optimization.zone_candidate_provider import ZoneCandidateProvider
from pini_desktop.services.editor.optimization.zone_definition import ZoneDefinition
from pini_desktop.services.editor.optimization.zone_score import ZoneScore, ZoneScoreCalculator

@dataclass(frozen=True)
class ZoneOptimizationSuggestion:
    session_id: int
    day: int
    period: int
    estimated_delta: float
    title: str

@dataclass(frozen=True)
class ZoneOptimizationResult:
    zone: ZoneDefinition
    before: ZoneScore
    suggestions: tuple[ZoneOptimizationSuggestion, ...]

    @property
    def best_delta(self) -> float:
        return max((item.estimated_delta for item in self.suggestions), default=0.0)

class ZoneOptimizer:
    def __init__(self, provider=None, score_calculator=None, candidate_builder=None, score_estimator=None):
        self.provider = provider or ZoneCandidateProvider()
        self.score_calculator = score_calculator or ZoneScoreCalculator()
        self.candidate_builder = candidate_builder or CandidateBuilder()
        self.score_estimator = score_estimator or ScoreEstimator()

    def optimize(self, zone: ZoneDefinition, limit: int = 5) -> ZoneOptimizationResult:
        sessions = self.provider.list_sessions(zone)
        before = self.score_calculator.calculate(sessions)
        suggestions = []
        for session in sessions:
            candidates = self.candidate_builder.build_move_candidates(session.id, session.day, session.period, radius=1)
            for candidate in candidates:
                estimated = self.score_estimator.estimate(candidate, session.day, session.period, before.score)
                if estimated.delta > 0:
                    suggestions.append(ZoneOptimizationSuggestion(session.id, candidate.day, candidate.period, estimated.delta, candidate.title))
        suggestions.sort(key=lambda item: item.estimated_delta, reverse=True)
        return ZoneOptimizationResult(zone, before, tuple(suggestions[:limit]))
