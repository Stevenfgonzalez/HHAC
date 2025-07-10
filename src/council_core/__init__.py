"""
Council Core Package

The central orchestrator that manages consensus between all seven domains.
Handles the cross-regulation mechanism and synthesizes recommendations.
"""

from .council import HHACCouncil
from .consensus import ConsensusEngine
from .synthesis import RecommendationSynthesizer

__all__ = ["HHACCouncil", "ConsensusEngine", "RecommendationSynthesizer"] 