"""
HHAC Domains Package

This package contains the seven specialized AI domains that work together
to provide holistic recommendations through the council core.
"""

from .base_domain import BaseDomain, DomainResponse, DomainMetrics
from .mind import MindDomain
from .body import BodyDomain
from .fuel import FuelDomain
from .rest import RestDomain
from .belong import BelongDomain
from .safety import SafetyDomain
from .purpose import PurposeDomain

__all__ = [
    "BaseDomain",
    "DomainResponse", 
    "DomainMetrics",
    "MindDomain",
    "BodyDomain",
    "FuelDomain",
    "RestDomain",
    "BelongDomain",
    "SafetyDomain",
    "PurposeDomain"
] 