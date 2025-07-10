"""
HHAC Council - Main Orchestrator

The central council that manages all seven domains and ensures consensus
before any recommendation reaches the user. This is the core of the
cross-regulation mechanism.
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass

from ..domains import (
    MindDomain, BodyDomain, FuelDomain, RestDomain, 
    BelongDomain, SafetyDomain, PurposeDomain,
    DomainResponse, ConsensusLevel
)


@dataclass
class UserContext:
    """User context and current state"""
    user_id: str
    current_state: Dict[str, Any]
    preferences: Dict[str, Any]
    history: List[Dict[str, Any]]
    timestamp: datetime


@dataclass
class CouncilResponse:
    """Final response from the council after consensus"""
    recommendation: str
    reasoning: str
    alternatives: List[str]
    consensus_level: str
    domain_insights: Dict[str, str]
    safety_concerns: List[str]
    confidence: float
    timestamp: datetime


class HHACCouncil:
    """
    Healing Hand AI Council - Main Orchestrator
    
    Manages the seven specialized domains and ensures consensus through
    the cross-regulation mechanism. No recommendation reaches the user
    without passing through all domains for evaluation.
    """
    
    def __init__(self):
        """Initialize the council with all seven domains"""
        self.domains = {
            "mind": MindDomain(),
            "body": BodyDomain(),
            "fuel": FuelDomain(),
            "rest": RestDomain(),
            "belong": BelongDomain(),
            "safety": SafetyDomain(),
            "purpose": PurposeDomain()
        }
        
        self.consensus_engine = ConsensusEngine()
        self.synthesizer = RecommendationSynthesizer()
        
        # Track council state
        self.session_count = 0
        self.last_consensus_time = None
        
    async def get_recommendation(self, user_input: str, context: UserContext) -> CouncilResponse:
        """
        Get a holistic recommendation through the council consensus process.
        
        Args:
            user_input: The user's input text
            context: Current user context and state
            
        Returns:
            CouncilResponse with consensus recommendation
        """
        self.session_count += 1
        
        # Step 1: Get individual domain evaluations
        domain_responses = await self._evaluate_all_domains(user_input, context)
        
        # Step 2: Check for safety blocks first (Safety domain has veto power)
        safety_response = domain_responses.get("safety")
        if safety_response and safety_response.consensus_level == ConsensusLevel.SAFETY_BLOCK:
            return self._handle_safety_block(safety_response, context)
        
        # Step 3: Run consensus protocol
        consensus_result = await self.consensus_engine.evaluate_consensus(
            domain_responses, context
        )
        
        # Step 4: Synthesize final recommendation
        final_recommendation = await self.synthesizer.synthesize_recommendation(
            domain_responses, consensus_result, context
        )
        
        # Step 5: Update council state
        self.last_consensus_time = datetime.now()
        
        return final_recommendation
    
    async def _evaluate_all_domains(self, user_input: str, context: UserContext) -> Dict[str, DomainResponse]:
        """Evaluate user input through all seven domains"""
        domain_responses = {}
        
        # Update all domains with current context
        for domain_name, domain in self.domains.items():
            domain.update_context(context.current_state)
        
        # Get evaluations from all domains concurrently
        evaluation_tasks = []
        for domain_name, domain in self.domains.items():
            task = domain.evaluate_input(user_input, context.current_state)
            evaluation_tasks.append((domain_name, task))
        
        # Wait for all domain evaluations to complete
        for domain_name, task in evaluation_tasks:
            try:
                response = await task
                domain_responses[domain_name] = response
            except Exception as e:
                # Log error and create fallback response
                print(f"Error in {domain_name} domain: {e}")
                domain_responses[domain_name] = self._create_fallback_response(domain_name)
        
        return domain_responses
    
    def _handle_safety_block(self, safety_response: DomainResponse, context: UserContext) -> CouncilResponse:
        """Handle safety block - highest priority"""
        return CouncilResponse(
            recommendation=safety_response.recommendation,
            reasoning=f"SAFETY BLOCK: {safety_response.reasoning}",
            alternatives=safety_response.alternatives,
            consensus_level="safety_block",
            domain_insights={"safety": safety_response.reasoning},
            safety_concerns=safety_response.safety_concerns,
            confidence=safety_response.confidence,
            timestamp=datetime.now()
        )
    
    def _create_fallback_response(self, domain_name: str) -> DomainResponse:
        """Create a fallback response if a domain fails"""
        from ..domains.base_domain import DomainType, DomainMetrics, ConsensusLevel
        
        return DomainResponse(
            domain_type=DomainType(domain_name),
            recommendation="Domain temporarily unavailable",
            reasoning="Technical issue in domain evaluation",
            consensus_level=ConsensusLevel.NEUTRAL,
            metrics=DomainMetrics(
                domain_type=DomainType(domain_name),
                confidence_score=0.0,
                urgency_level=0.0,
                impact_score=0.5,
                data_quality=0.0,
                timestamp=datetime.now(),
                metadata={"error": "fallback_response"}
            ),
            alternatives=[],
            safety_concerns=[],
            confidence=0.0,
            timestamp=datetime.now()
        )
    
    async def evaluate_recommendation(self, recommendation: str, context: UserContext) -> Dict[str, ConsensusLevel]:
        """Evaluate a proposed recommendation through all domains"""
        domain_evaluations = {}
        
        # Get evaluations from all domains concurrently
        evaluation_tasks = []
        for domain_name, domain in self.domains.items():
            task = domain.evaluate_recommendation(recommendation, context.current_state)
            evaluation_tasks.append((domain_name, task))
        
        # Wait for all evaluations to complete
        for domain_name, task in evaluation_tasks:
            try:
                consensus_level = await task
                domain_evaluations[domain_name] = consensus_level
            except Exception as e:
                print(f"Error evaluating recommendation in {domain_name} domain: {e}")
                domain_evaluations[domain_name] = ConsensusLevel.NEUTRAL
        
        return domain_evaluations
    
    def get_council_status(self) -> Dict[str, Any]:
        """Get current status of the council"""
        domain_status = {}
        for domain_name, domain in self.domains.items():
            domain_status[domain_name] = domain.get_domain_info()
        
        return {
            "session_count": self.session_count,
            "last_consensus_time": self.last_consensus_time.isoformat() if self.last_consensus_time else None,
            "domains": domain_status,
            "council_version": "1.0.0"
        }
    
    def update_user_context(self, user_id: str, new_context: Dict[str, Any]) -> None:
        """Update user context across all domains"""
        for domain in self.domains.values():
            domain.update_context(new_context)
    
    def get_domain_metrics(self, context: UserContext) -> Dict[str, Any]:
        """Get metrics from all domains"""
        metrics = {}
        for domain_name, domain in self.domains.items():
            metrics[domain_name] = domain.get_domain_metrics(context.current_state)
        return metrics


# Import these after the main class to avoid circular imports
from .consensus import ConsensusEngine
from .synthesis import RecommendationSynthesizer 