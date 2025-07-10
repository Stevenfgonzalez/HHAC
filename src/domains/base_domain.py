"""
Base Domain Class for HHAC System

Defines the interface that all seven specialized domains must implement.
Each domain operates autonomously while sharing data through the council core.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from enum import Enum
from pydantic import BaseModel
from dataclasses import dataclass
import uuid
from datetime import datetime


class DomainType(Enum):
    """Enumeration of the seven HHAC domains"""
    MIND = "mind"
    BODY = "body"
    FUEL = "fuel"
    REST = "rest"
    BELONG = "belong"
    SAFETY = "safety"
    PURPOSE = "purpose"


class ConsensusLevel(Enum):
    """Levels of consensus agreement"""
    STRONG_AGREEMENT = "strong_agreement"
    AGREEMENT = "agreement"
    NEUTRAL = "neutral"
    DISAGREEMENT = "disagreement"
    STRONG_DISAGREEMENT = "strong_disagreement"
    SAFETY_BLOCK = "safety_block"


@dataclass
class DomainMetrics:
    """Metrics and data specific to each domain"""
    domain_type: DomainType
    confidence_score: float  # 0.0 to 1.0
    urgency_level: float    # 0.0 to 1.0
    impact_score: float     # 0.0 to 1.0
    data_quality: float     # 0.0 to 1.0
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass
class DomainResponse:
    """Response from a domain evaluation"""
    domain_type: DomainType
    recommendation: str
    reasoning: str
    consensus_level: ConsensusLevel
    metrics: DomainMetrics
    alternatives: List[str]
    safety_concerns: List[str]
    confidence: float
    timestamp: datetime


class BaseDomain(ABC):
    """
    Abstract base class for all HHAC domains.
    
    Each domain specializes in one aspect of human wellbeing and provides
    recommendations based on its expertise while considering the whole person.
    """
    
    def __init__(self, domain_type: DomainType):
        self.domain_type = domain_type
        self.domain_id = str(uuid.uuid4())
        self.last_updated = datetime.now()
        self._initialize_domain()
    
    @abstractmethod
    def _initialize_domain(self) -> None:
        """Initialize domain-specific models, data, and configurations"""
        pass
    
    @abstractmethod
    async def evaluate_input(self, user_input: str, context: Dict[str, Any]) -> DomainResponse:
        """
        Evaluate user input from this domain's perspective.
        
        Args:
            user_input: The user's input text
            context: Current user context and state
            
        Returns:
            DomainResponse with recommendation and metrics
        """
        pass
    
    @abstractmethod
    async def evaluate_recommendation(self, recommendation: str, context: Dict[str, Any]) -> ConsensusLevel:
        """
        Evaluate a proposed recommendation from this domain's perspective.
        
        Args:
            recommendation: The proposed recommendation to evaluate
            context: Current user context and state
            
        Returns:
            ConsensusLevel indicating agreement/disagreement
        """
        pass
    
    @abstractmethod
    def get_domain_metrics(self, context: Dict[str, Any]) -> DomainMetrics:
        """
        Get current metrics for this domain based on user context.
        
        Args:
            context: Current user context and state
            
        Returns:
            DomainMetrics with current domain state
        """
        pass
    
    @abstractmethod
    def get_safety_concerns(self, recommendation: str, context: Dict[str, Any]) -> List[str]:
        """
        Identify any safety concerns from this domain's perspective.
        
        Args:
            recommendation: The recommendation to check
            context: Current user context and state
            
        Returns:
            List of safety concerns (empty if none)
        """
        pass
    
    def update_context(self, context: Dict[str, Any]) -> None:
        """
        Update domain's understanding of user context.
        
        Args:
            context: Updated user context
        """
        self.last_updated = datetime.now()
        self._process_context_update(context)
    
    @abstractmethod
    def _process_context_update(self, context: Dict[str, Any]) -> None:
        """Process context updates specific to this domain"""
        pass
    
    def get_domain_info(self) -> Dict[str, Any]:
        """Get information about this domain"""
        return {
            "domain_type": self.domain_type.value,
            "domain_id": self.domain_id,
            "last_updated": self.last_updated.isoformat(),
            "description": self.get_domain_description()
        }
    
    @abstractmethod
    def get_domain_description(self) -> str:
        """Get a description of this domain's focus and expertise"""
        pass
    
    def is_safety_domain(self) -> bool:
        """Check if this is the safety domain (has special privileges)"""
        return self.domain_type == DomainType.SAFETY 